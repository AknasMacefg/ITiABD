import 'package:intl/date_symbol_data_local.dart';
import 'package:flutter/material.dart';

import 'models/search_result.dart';
import 'models/schedule_entry.dart';
import 'services/schedule_api.dart';

void main() {
  WidgetsFlutterBinding.ensureInitialized();
  initializeDateFormatting('ru', null).then((_) {
    runApp(const ScheduleApp());
  });
}

class ScheduleApp extends StatelessWidget {
  const ScheduleApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Расписание',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.lightBlue),
        useMaterial3: true,
      ),
      home: const SchedulePage(),
    );
  }
}

enum SearchScope { group, teacher, room }

enum ResultView { list, grid, calendar }

class SchedulePage extends StatefulWidget {
  const SchedulePage({super.key});

  @override
  State<SchedulePage> createState() => _SchedulePageState();
}

class _SchedulePageState extends State<SchedulePage> {
  final TextEditingController _searchController = TextEditingController();
  final ScheduleApi _scheduleApi = ScheduleApi();

  SearchScope _searchScope = SearchScope.group;
  ResultView _resultView = ResultView.list;
  late DateTime _weekStart;
  String _query = '';
  final Set<SearchResult> _selectedTargets = <SearchResult>{};
  List<SearchResult> _searchResults = <SearchResult>[];
  List<Post> _schedule = <Post>[];
  bool _isLoadingSearch = false;
  bool _isLoadingSchedule = false;
  String? _errorMessage;
  int _searchRequestToken = 0;
  int _scheduleRequestToken = 0;

  @override
  void initState() {
    super.initState();
    _weekStart = _mondayOf(DateTime.now());
    _searchController.addListener(() {
      setState(() {
        _query = _searchController.text.trim();
      });
      _refreshSearchResults();
    });
  }

  @override
  void dispose() {
    _searchController.dispose();
    super.dispose();
  }

  DateTime _mondayOf(DateTime date) {
    return DateTime(date.year, date.month, date.day)
        .subtract(Duration(days: date.weekday - DateTime.monday));
  }

  String _formatDate(DateTime date) {
    final String day = date.day.toString().padLeft(2, '0');
    final String month = date.month.toString().padLeft(2, '0');
    return '$day.$month.${date.year}';
  }

  String _scopeLabel(SearchScope scope) {
    switch (scope) {
      case SearchScope.group:
        return 'Группа';
      case SearchScope.teacher:
        return 'Преподаватель';
      case SearchScope.room:
        return 'Аудитория';
    }
  }

  String _viewLabel(ResultView view) {
    switch (view) {
      case ResultView.list:
        return 'Список';
      case ResultView.grid:
        return 'Сетка';
      case ResultView.calendar:
        return 'Календарь';
    }
  }

  void _selectScope(SearchScope scope) {
    setState(() {
      _searchScope = scope;
      _selectedTargets.clear();
      _searchResults = <SearchResult>[];
      _schedule = <Post>[];
      _errorMessage = null;
    });
    _refreshSearchResults();
  }

  void _selectView(ResultView view) {
    setState(() {
      _resultView = view;
    });
  }

  void _previousWeek() {
    setState(() {
      _weekStart = _weekStart.subtract(const Duration(days: 7));
    });
    _refreshSchedule();
  }

  void _nextWeek() {
    setState(() {
      _weekStart = _weekStart.add(const Duration(days: 7));
    });
    _refreshSchedule();
  }

  Future<void> _pickWeek() async {
    final DateTime now = DateTime.now();
    final DateTime? picked = await showDatePicker(
      context: context,
      initialDate: _weekStart,
      firstDate: DateTime(now.year - 1),
      lastDate: DateTime(now.year + 1),
      helpText: 'Выбор недели',
    );

    if (picked == null) {
      return;
    }

    setState(() {
      _weekStart = _mondayOf(picked);
    });
    _refreshSchedule();
  }

  void _resetFilters() {
    setState(() {
      _searchController.clear();
      _searchScope = SearchScope.group;
      _resultView = ResultView.list;
      _weekStart = _mondayOf(DateTime.now());
      _query = '';
      _selectedTargets.clear();
      _searchResults = <SearchResult>[];
      _schedule = <Post>[];
      _errorMessage = null;
    });
    _refreshSchedule();
  }

  Future<void> _refreshSearchResults() async {
    final String query = _query;
    final int requestToken = ++_searchRequestToken;

    if (query.isEmpty) {
      if (!mounted) {
        return;
      }
      setState(() {
        _searchResults = <SearchResult>[];
        _isLoadingSearch = false;
        _errorMessage = null;
      });
      return;
    }

    if (!mounted) {
      return;
    }
    setState(() {
      _isLoadingSearch = true;
      _errorMessage = null;
    });

    try {
      final List<SearchResult> results;
      switch (_searchScope) {
        case SearchScope.group:
          results = await _scheduleApi.searchGroups(query);
          break;
        case SearchScope.teacher:
          results = await _scheduleApi.searchTeachers(query);
          break;
        case SearchScope.room:
          results = await _scheduleApi.searchRooms(query);
          break;
      }

      if (!mounted || requestToken != _searchRequestToken) {
        return;
      }
      setState(() {
        _searchResults = results;
        _isLoadingSearch = false;
      });
    } catch (e) {
      print('Search error: $e');
      if (!mounted || requestToken != _searchRequestToken) {
        return;
      }
      setState(() {
        _searchResults = <SearchResult>[];
        _isLoadingSearch = false;
        _errorMessage = 'Не удалось загрузить результаты поиска';
      });
    }
  }

  Future<void> _refreshSchedule() async {
    if (_selectedTargets.isEmpty) {
      if (!mounted) {
        return;
      }
      setState(() {
        _schedule = <Post>[];
        _isLoadingSchedule = false;
        _errorMessage = null;
      });
      return;
    }

    final int requestToken = ++_scheduleRequestToken;
    if (!mounted) {
      return;
    }
    setState(() {
      _isLoadingSchedule = true;
      _errorMessage = null;
    });

    try {
      final List<Post> schedule;
      final List<SearchResult> selectedTargets = _selectedTargets.toList();
      switch (_searchScope) {
        case SearchScope.group:
          schedule = await _scheduleApi.getScheduleForGroup(
            selected: selectedTargets,
            weekStart: _weekStart,
          );
          break;
        case SearchScope.teacher:
          schedule = await _scheduleApi.getScheduleForPerson(
            selected: selectedTargets,
            weekStart: _weekStart,
          );
          break;
        case SearchScope.room:
          schedule = await _scheduleApi.getScheduleForAuditorium(
            selected: selectedTargets,
            weekStart: _weekStart,
          );
          break;
      }

      if (!mounted || requestToken != _scheduleRequestToken) {
        return;
      }
      setState(() {
        _schedule = schedule;
        _isLoadingSchedule = false;
      });
    } catch (e) {
      print('Schedule error: $e');
      if (!mounted || requestToken != _scheduleRequestToken) {
        return;
      }
      setState(() {
        _schedule = <Post>[];
        _isLoadingSchedule = false;
        _errorMessage = 'Не удалось загрузить расписание';
      });
    }
  }

  Widget _buildSearchResults() {
    if (_query.isEmpty) {
      return const SizedBox.shrink();
    }

    if (_isLoadingSearch) {
      return const Padding(
        padding: EdgeInsets.only(top: 8),
        child: LinearProgressIndicator(),
      );
    }

    if (_searchResults.isEmpty) {
      return Padding(
        padding: const EdgeInsets.only(top: 8),
        child: Text(
          'Ничего не найдено',
          style: TextStyle(color: Theme.of(context).colorScheme.outline),
        ),
      );
    }

    return Container(
      margin: const EdgeInsets.only(top: 8),
      constraints: const BoxConstraints(maxHeight: 200),
      decoration: BoxDecoration(
        border: Border.all(color: Theme.of(context).dividerColor),
        borderRadius: BorderRadius.circular(12),
      ),
      child: ListView.separated(
        shrinkWrap: true,
        itemCount: _searchResults.length,
        separatorBuilder: (_, __) => const Divider(height: 1),
        itemBuilder: (BuildContext context, int index) {
          final SearchResult result = _searchResults[index];
          final bool selected = _selectedTargets.contains(result);
          return CheckboxListTile(
            value: selected,
            title: Text(result.label),
            subtitle: Text(
              result.description,
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
              style: TextStyle(fontSize: 12, color: Theme.of(context).colorScheme.outline),
            ),
            controlAffinity: ListTileControlAffinity.leading,
            onChanged: (_) {
              setState(() {
                if (selected) {
                  _selectedTargets.remove(result);
                } else {
                  _selectedTargets.add(result);
                }
              });
              _refreshSchedule();
            },
          );
        },
      ),
    );
  }

  Widget _buildSelectedChips() {
    if (_selectedTargets.isEmpty) {
      return const SizedBox.shrink();
    }

    return Padding(
      padding: const EdgeInsets.only(top: 8, bottom: 8),
      child: Wrap(
        spacing: 8,
        runSpacing: 4,
        children: _selectedTargets.map((SearchResult target) {
          return Chip(
            label: Text(target.label),
            onDeleted: () {
              setState(() {
                _selectedTargets.remove(target);
              });
              _refreshSchedule();
            },
          );
        }).toList(),
      ),
    );
  }

  Widget _buildListBody() {
    return ListView.separated(
      itemCount: _schedule.length,
      separatorBuilder: (_, __) => const SizedBox(height: 8),
      itemBuilder: (BuildContext context, int index) {
        final Post lesson = _schedule[index];
        return Card(
          child: ListTile(
            title: Text(lesson.discipline),
            subtitle: Text(
              '${lesson.beginLesson} - ${lesson.endLesson}\n${lesson.lecturer} • ${lesson.auditorium} • ${lesson.date}',
            ),
            isThreeLine: true,
          ),
        );
      },
    );
  }

  Widget _buildGridBody() {
    return GridView.builder(
      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 2,
        crossAxisSpacing: 12,
        mainAxisSpacing: 12,
        childAspectRatio: 1.15,
      ),
      itemCount: _schedule.length,
      itemBuilder: (BuildContext context, int index) {
        final Post lesson = _schedule[index];
        return Card(
          child: Padding(
            padding: const EdgeInsets.all(12),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  lesson.discipline,
                  style: Theme.of(context).textTheme.titleSmall,
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                ),
                const SizedBox(height: 8),
                Text('${lesson.beginLesson} - ${lesson.endLesson}'),
                const SizedBox(height: 8),
                Text(
                  lesson.lecturer,
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                ),
                const Spacer(),
                Text(
                  '${lesson.auditorium} • ${lesson.date}',
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                ),
              ],
            ),
          ),
        );
      },
    );
  }

  DateTime _dateOnly(DateTime date) => DateTime(date.year, date.month, date.day);

  Widget _buildCalendarBody() {
    final DateTime monthStart = DateTime(_weekStart.year, _weekStart.month, 1);
    final DateTime monthEnd = DateTime(_weekStart.year, _weekStart.month + 1, 0);
    final int leadingEmptyDays = monthStart.weekday - DateTime.monday;
    final int totalCells = ((leadingEmptyDays + monthEnd.day) / 7).ceil() * 7;
    final DateTime selectedWeekEnd = _weekStart.add(const Duration(days: 6));

    return GridView.builder(
      gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 7,
        mainAxisSpacing: 6,
        crossAxisSpacing: 6,
        childAspectRatio: 0.95,
      ),
      itemCount: totalCells,
      itemBuilder: (BuildContext context, int index) {
        final int dayNumber = index - leadingEmptyDays + 1;
        if (dayNumber < 1 || dayNumber > monthEnd.day) {
          return const SizedBox.shrink();
        }

        final DateTime day = DateTime(monthStart.year, monthStart.month, dayNumber);
        final bool inCurrentWeek = !day.isBefore(_weekStart) && !day.isAfter(selectedWeekEnd);
        final List<Post> lessonsForDay = _schedule
            .where((Post lesson) => lesson.dateValue != null && _dateOnly(lesson.dateValue!) == day)
            .toList();

        return Container(
          padding: const EdgeInsets.all(6),
          decoration: BoxDecoration(
            color: inCurrentWeek
                ? Theme.of(context).colorScheme.primaryContainer
                : Theme.of(context).colorScheme.surfaceContainerHighest,
            borderRadius: BorderRadius.circular(10),
            border: Border.all(
              color: inCurrentWeek
                  ? Theme.of(context).colorScheme.primary
                  : Theme.of(context).dividerColor,
            ),
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                '$dayNumber',
                style: Theme.of(context).textTheme.labelLarge,
              ),
              const SizedBox(height: 4),
              if (lessonsForDay.isEmpty)
                Text(
                  'Нет пар',
                  style: Theme.of(context).textTheme.bodySmall,
                )
              else
                ...lessonsForDay.take(2).map((Post lesson) {
                  return Padding(
                    padding: const EdgeInsets.only(bottom: 4),
                    child: Text(
                      lesson.discipline,
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                      style: Theme.of(context).textTheme.bodySmall,
                    ),
                  );
                }),
            ],
          ),
        );
      },
    );
  }

  Widget _buildBody() {
    if (_selectedTargets.isEmpty) {
      return Center(
        child: Text(
          'Выберите значение',
          style: TextStyle(color: Theme.of(context).colorScheme.outline),
        ),
      );
    }

    if (_isLoadingSchedule) {
      return const Center(child: CircularProgressIndicator());
    }

    if (_schedule.isEmpty) {
      return Center(
        child: Text(
          'Нет данных',
          style: TextStyle(color: Theme.of(context).colorScheme.outline),
        ),
      );
    }

    switch (_resultView) {
      case ResultView.list:
        return _buildListBody();
      case ResultView.grid:
        return _buildGridBody();
      case ResultView.calendar:
        return _buildCalendarBody();
    }
  }

  @override
  Widget build(BuildContext context) {
    final DateTime weekEnd = _weekStart.add(const Duration(days: 6));

    return Scaffold(
      appBar: AppBar(
        title: const Text('Расписание'),
      ),
      body: SingleChildScrollView(
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Scope Selection
              Text(
                'Тип поиска:',
                style: Theme.of(context).textTheme.titleSmall,
              ),
              const SizedBox(height: 8),
              SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: Row(
                  children: [
                    for (final SearchScope scope in SearchScope.values)
                      Padding(
                        padding: const EdgeInsets.only(right: 8),
                        child: FilterChip(
                          label: Text(_scopeLabel(scope)),
                          selected: _searchScope == scope,
                          onSelected: (_) => _selectScope(scope),
                        ),
                      ),
                  ],
                ),
              ),
              const SizedBox(height: 16),

              // Search Input
              TextField(
                controller: _searchController,
                decoration: InputDecoration(
                  labelText: 'Поиск',
                  prefixIcon: const Icon(Icons.search),
                  border: OutlineInputBorder(borderRadius: BorderRadius.circular(8)),
                ),
              ),

              // Search Results Dropdown
              _buildSearchResults(),
              _buildSelectedChips(),

              const SizedBox(height: 16),

              // Result View Selection
              Text(
                'Вид результатов:',
                style: Theme.of(context).textTheme.titleSmall,
              ),
              const SizedBox(height: 8),
              SingleChildScrollView(
                scrollDirection: Axis.horizontal,
                child: Row(
                  children: [
                    for (final ResultView view in ResultView.values)
                      Padding(
                        padding: const EdgeInsets.only(right: 8),
                        child: FilterChip(
                          label: Text(_viewLabel(view)),
                          selected: _resultView == view,
                          onSelected: (_) => _selectView(view),
                        ),
                      ),
                  ],
                ),
              ),
              const SizedBox(height: 16),

              // Week Controls
              Text(
                'Выбор недели: ${_formatDate(_weekStart)} - ${_formatDate(weekEnd)}',
                style: Theme.of(context).textTheme.titleSmall,
              ),
              const SizedBox(height: 8),
              Wrap(
                spacing: 8,
                runSpacing: 8,
                children: [
                  IconButton(
                    icon: const Icon(Icons.arrow_back),
                    onPressed: _previousWeek,
                    tooltip: 'Предыдущая неделя',
                  ),
                  TextButton.icon(
                    icon: const Icon(Icons.calendar_today),
                    label: const Text('Выбрать'),
                    onPressed: _pickWeek,
                  ),
                  IconButton(
                    icon: const Icon(Icons.arrow_forward),
                    onPressed: _nextWeek,
                    tooltip: 'Следующая неделя',
                  ),
                  TextButton.icon(
                    icon: const Icon(Icons.restart_alt),
                    label: const Text('Сброс'),
                    onPressed: _resetFilters,
                  ),
                ],
              ),
              const SizedBox(height: 16),

              // Error Message
              if (_errorMessage != null)
                Padding(
                  padding: const EdgeInsets.only(bottom: 16),
                  child: Text(
                    _errorMessage!,
                    style: TextStyle(color: Theme.of(context).colorScheme.error),
                  ),
                ),

              // Results Body
              SizedBox(
                height: 400,
                child: _buildBody(),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
