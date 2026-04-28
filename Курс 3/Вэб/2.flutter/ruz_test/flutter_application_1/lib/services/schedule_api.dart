import 'package:dio/dio.dart';
import '../models/search_result.dart';
import '../models/schedule_entry.dart';

class ScheduleApi {
  final Dio _dio = Dio(
    BaseOptions(
      baseUrl: 'https://ruz.fa.ru/api',
      connectTimeout: const Duration(seconds: 10),
      receiveTimeout: const Duration(seconds: 10),
    ),
  );

  List<dynamic> _extractItems(dynamic data) {
    if (data is List) {
      return data;
    }

    if (data is Map) {
      final Map<String, dynamic> map = Map<String, dynamic>.from(data);
      final Object? candidates = map['data'] ?? map['result'] ?? map['results'] ?? map['items'];
      if (candidates is List) {
        return candidates;
      }

      for (final Object? value in map.values) {
        if (value is List) {
          return value;
        }
      }
    }

    return <dynamic>[];
  }

  Future<List<SearchResult>> _searchByType(String type, String query) async {
    final response = await _dio.get(
      '/search',
      queryParameters: {
        'term': query,
        'type': type,
      },
    );

    if (response.statusCode != 200) {
      return <SearchResult>[];
    }

    final List<dynamic> data = _extractItems(response.data);
    return data.map((dynamic item) {
      if (item is Map<String, dynamic>) {
        return SearchResult.fromJson(item);
      }
      if (item is Map) {
        return SearchResult.fromJson(Map<String, dynamic>.from(item));
      }
      return SearchResult.fromJson(<String, dynamic>{});
    }).toList();
  }

  Future<List<SearchResult>> searchGroups(String query) async {
    return _searchByType('group', query);
  }

  Future<List<SearchResult>> searchTeachers(String query) async {
    return _searchByType('person', query);
  }

  Future<List<SearchResult>> searchRooms(String query) async {
    return _searchByType('auditorium', query);
  }

  Future<List<Post>> _getScheduleByPath({
    required String path,
    required DateTime weekStart,
    required DateTime weekEnd,
  }) async {
    final response = await _dio.get(
      path,
      queryParameters: {
        'start': weekStart.toIso8601String().split('T')[0],
        'finish': weekEnd.toIso8601String().split('T')[0],
      },
    );

    if (response.statusCode != 200) {
      return <Post>[];
    }

    final List<dynamic> data = _extractItems(response.data);
    return data.map((dynamic item) {
      if (item is Map<String, dynamic>) {
        return Post.fromJson(item);
      }
      if (item is Map) {
        return Post.fromJson(Map<String, dynamic>.from(item));
      }
      return Post.fromJson(<String, dynamic>{});
    }).toList();
  }

  Future<List<Post>> getScheduleForGroup({
    required List<SearchResult> selected,
    required DateTime weekStart,
  }) {
    final ids = selected.map((s) => s.id).join(',');
    return _getScheduleByPath(
      path: '/schedule/group/$ids',
      weekStart: weekStart,
      weekEnd: weekStart.add(const Duration(days: 6)),
    );
  }

  Future<List<Post>> getScheduleForPerson({
    required List<SearchResult> selected,
    required DateTime weekStart,
  }) {
    final ids = selected.map((s) => s.id).join(',');
    return _getScheduleByPath(
      path: '/schedule/person/$ids',
      weekStart: weekStart,
      weekEnd: weekStart.add(const Duration(days: 6)),
    );
  }

  Future<List<Post>> getScheduleForAuditorium({
    required List<SearchResult> selected,
    required DateTime weekStart,
  }) {
    final ids = selected.map((s) => s.id).join(',');
    return _getScheduleByPath(
      path: '/schedule/auditorium/$ids',
      weekStart: weekStart,
      weekEnd: weekStart.add(const Duration(days: 6)),
    );
  }
}
