import 'package:intl/intl.dart';

class Post {
  final int id;
  final String discipline;
  final String kindOfWork;
  final String lecturer;
  final String auditorium;
  final String building;
  final String group;
  final String beginLesson;
  final String endLesson;
  final String date;
  final DateTime? dateValue;

  Post({
    required this.id,
    required this.discipline,
    required this.kindOfWork,
    required this.lecturer,
    required this.auditorium,
    required this.building,
    required this.group,
    required this.beginLesson,
    required this.endLesson,
    required this.date,
    this.dateValue,
  });

  factory Post.fromJson(Map<String, dynamic> json) {
    final String rawDate = (json['date'] ?? '').toString();
    final DateTime? parsedDate = rawDate.isEmpty ? null : DateTime.tryParse(rawDate);
    return Post(
      id: (json['lessonid'] as num?)?.toInt() ?? 0,
      discipline: (json['discipline'] ?? '').toString(),
      kindOfWork: (json['kindOfWork'] ?? '').toString(),
      lecturer: (json['lecturer'] ?? '').toString(),
      auditorium: (json['auditorium'] ?? '').toString(),
      building: (json['building'] ?? '').toString(),
      group: (json['group'] ?? '').toString(),
      beginLesson: (json['beginLesson'] ?? '').toString(),
      endLesson: (json['endLesson'] ?? '').toString(),
      date: rawDate.isEmpty
          ? ''
          : DateFormat.yMMMMEEEEd('ru')
              .format(DateFormat('y-MM-dd').parse(rawDate)),
      dateValue: parsedDate,
    );
  }

}
