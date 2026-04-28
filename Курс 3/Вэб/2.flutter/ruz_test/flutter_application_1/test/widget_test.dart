import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';

import 'package:flutter_application_1/main.dart';

void main() {
  testWidgets('shows schedule screen controls', (WidgetTester tester) async {
    await tester.pumpWidget(const ScheduleApp());

    expect(find.text('Расписание'), findsOneWidget);
    expect(find.text('Группа'), findsOneWidget);
    expect(find.text('Преподаватель'), findsOneWidget);
    expect(find.text('Аудитория'), findsOneWidget);
    expect(find.text('Поиск'), findsOneWidget);
    expect(find.text('Выбрать'), findsOneWidget);
    expect(find.text('Сброс'), findsOneWidget);
    expect(find.text('Список'), findsOneWidget);
    expect(find.text('Сетка'), findsOneWidget);
    expect(find.text('Календарь'), findsOneWidget);
  });

  testWidgets('updates scope and view chips', (WidgetTester tester) async {
    await tester.pumpWidget(const ScheduleApp());

    final Finder teacherChip = find.widgetWithText(FilterChip, 'Преподаватель');
    final Finder gridChip = find.widgetWithText(FilterChip, 'Сетка');

    await tester.tap(teacherChip);
    await tester.pump();
    expect(tester.widget<FilterChip>(teacherChip).selected, isTrue);
    expect(tester.widget<FilterChip>(find.widgetWithText(FilterChip, 'Группа')).selected, isFalse);

    await tester.tap(gridChip);
    await tester.pump();
    expect(tester.widget<FilterChip>(gridChip).selected, isTrue);
    expect(tester.widget<FilterChip>(find.widgetWithText(FilterChip, 'Список')).selected, isFalse);
  });

  testWidgets('resets scope and view to defaults', (WidgetTester tester) async {
    await tester.pumpWidget(const ScheduleApp());

    await tester.tap(find.widgetWithText(FilterChip, 'Преподаватель'));
    await tester.pump();
    await tester.tap(find.widgetWithText(FilterChip, 'Календарь'));
    await tester.pump();
    await tester.tap(find.text('Сброс'));
    await tester.pump();

    expect(tester.widget<FilterChip>(find.widgetWithText(FilterChip, 'Группа')).selected, isTrue);
    expect(tester.widget<FilterChip>(find.widgetWithText(FilterChip, 'Список')).selected, isTrue);
    expect(tester.widget<FilterChip>(find.widgetWithText(FilterChip, 'Преподаватель')).selected, isFalse);
    expect(tester.widget<FilterChip>(find.widgetWithText(FilterChip, 'Календарь')).selected, isFalse);
  });
}
