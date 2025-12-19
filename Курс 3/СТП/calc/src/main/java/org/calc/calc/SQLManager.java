package org.calc.calc;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.ss.usermodel.Workbook;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;

import java.io.FileOutputStream;
import java.io.IOException;
import java.sql.*;
import java.util.ArrayList;

/**
 * Вспомогательный класс для работы с базой данных PostgreSQL.
 *
 * <p>Отвечает за:</p>
 * <ul>
 *     <li>Установку и хранение соединения с БД</li>
 *     <li>Создание служебных таблиц пользователей и операций при первом запуске</li>
 *     <li>Выполнение типовых SQL‑запросов (INSERT/UPDATE/SELECT)</li>
 *     <li>Экспорт данных всех таблиц схемы в Excel‑файлы формата XLSX</li>
 * </ul>
 */
class SQLManager {
    /** Общий коннект к базе данных PostgreSQL. */
    protected static Connection conn;
    /** Имя схемы, в которой создаются служебные таблицы приложения. */
    protected static final String schemaname = "calc_db";
    static {
        try {

            String pass = "postgres";
            String user = "postgres";
            String db_name = "postgres";
            String port = "5432";
            String ip = "127.0.0.1";
            String url = "jdbc:postgresql://"+ip+":"+port+"/"+db_name;
            conn = DriverManager.getConnection(url, user, pass);
            Statement stmt = conn.createStatement();
            stmt.executeUpdate("CREATE SCHEMA IF NOT EXISTS " + schemaname);
            System.out.println("База данных подключена. Выбранная схема: " + schemaname);
            SQLQueryCreate(String.format("""
                    CREATE TABLE IF NOT EXISTS %s.users (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        email VARCHAR(255) UNIQUE NOT NULL,
                        login VARCHAR(100) UNIQUE NOT NULL,
                        hash_password VARCHAR(255) NOT NULL,
                        role VARCHAR(50) DEFAULT 'user' NOT NULL,
                        last_login_time TIMESTAMP WITH TIME ZONE,
                        last_logoff_time TIMESTAMP WITH TIME ZONE,
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
                    );""", schemaname));

            SQLQueryCreate(String.format("""
                    CREATE TABLE IF NOT EXISTS %s.operations (
                        id SERIAL PRIMARY KEY,
                        user_id INTEGER NOT NULL,
                        operation_type VARCHAR(100) NOT NULL,
                        input_data TEXT,
                        result TEXT,
                        created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
     
                        CONSTRAINT fk_operations_user
                            FOREIGN KEY (user_id)
                            REFERENCES %s.users(id)
                            ON DELETE CASCADE
                    );""", schemaname, schemaname));

        } catch (SQLException e) {
            System.out.println("Не удалось подключиться к базе данных! " + e);
            System.exit(0);
        }
    }

    /**
     * Выполняет SQL‑запрос на изменение данных (CREATE, INSERT, UPDATE, DELETE).
     *
     * @param query SQL‑запрос для выполнения
     */
    protected static void SQLQueryCreate(String query) {
        try {
            Statement stmt = conn.createStatement();
            stmt.executeUpdate(query);
            System.out.println("Данные успешно обновлены");
        } catch (SQLException e) {
            System.out.println("Ошибка при выполнении запроса: " + e.getMessage());
            System.out.println("Проблемный запрос: " + query);
        }
    }

    /**
     * Возвращает список таблиц в текущей схеме.
     *
     * @return {@link ResultSet} c именами таблиц или {@code null} в случае ошибки
     */
    private static ResultSet SQLSelectAllTable(){
        try {
            Statement stmt = conn.createStatement();
            return stmt.executeQuery("SELECT tablename FROM pg_tables WHERE schemaname = '" + schemaname + "'");
        }catch (SQLException e){
            return null;
        }
    }

    /**
     * Выводит в консоль список всех таблиц в схеме.
     *
     * @return {@code true}, если таблицы найдены и выведены; {@code false} при ошибке или отсутствии таблиц
     */
    protected static boolean SQLQuerySelectTable(){
        try {
            if (!SQLSelectAllTable().next() || SQLSelectAllTable() == null) {
                System.out.println("Создайте хотя бы одну таблицу! ");
                return false;
            }
            ResultSet rs = SQLSelectAllTable();
            System.out.println("Текущие таблицы: ");
            while (rs.next()) {
                System.out.println(rs.getString(1));
            }
            return true;
        }catch (SQLException e){
            System.out.println("Ошибка синтаксиса. " + e);
            return false;
        }
    }

    /**
     * Выполняет SELECT‑запрос и возвращает значение первого столбца первой строки результата.
     *
     * @param query SQL‑запрос SELECT
     * @return строковое значение первой ячейки результата или пустая строка, если данных нет либо произошла ошибка
     */
    protected static String SQLQuerySelectReturner(String query){
        try {
            Statement stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery(query);
            ResultSetMetaData rsmd = rs.getMetaData();
            int rowindex = 1;
            if (!rs.next()) {
                System.out.println("Не найдено результатов с таким запросом");
                return "";
            }
            return rs.getString(rowindex);
        }catch (SQLException e){
            System.out.println("Ошибка синтаксиса. " + e);
            return "";
        }
    }

    /**
     * Выполняет SELECT‑запрос и возвращает {@link ResultSet} с первой найденной строкой.
     * <p>Курсор уже смещён на первую строку результата.</p>
     *
     * @param query SQL‑запрос SELECT
     * @return {@link ResultSet} с первой записью или {@code null}, если ничего не найдено либо произошла ошибка
     */
    protected static ResultSet SQLQueryRowSelect(String query) {
        try {
            Statement stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery(query);
            ResultSetMetaData rsmd = rs.getMetaData();
            int rowindex = 1;
            if (!rs.next()) {
                System.out.println("Не найдено результатов с таким запросом");
                return null;
            }
            return rs;
        }catch (SQLException e){
            System.out.println("Ошибка синтаксиса. " + e);
            return null;
        }
    }

    /**
     * Выполняет SELECT‑запрос и построчно выводит результат в консоль.
     *
     * @param query SQL‑запрос SELECT
     * @return {@code false} (метод предназначен только для вывода, а не для логического результата)
     */
    protected static boolean SQLQuerySelect(String query) {
        try {
            Statement stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery(query);
            ResultSetMetaData rsmd = rs.getMetaData();
            int rowindex = 0;
            if (!rs.next()) {
                System.out.println("Не найдено результатов с таким ID");
                return false;
            }
            rs = stmt.executeQuery(query);
            while (rs.next()) {
                for (int x = 1; x <= rsmd.getColumnCount(); x++)
                {
                    if (rowindex == 0) {
                        System.out.printf("%-25s", rsmd.getColumnName(x));
                        if (x == rsmd.getColumnCount())
                        {
                            rowindex++;
                            x=1;
                            System.out.println();
                        } else continue;
                    }
                    TypeExtractor(null, rs, x, rsmd.getColumnClassName(x));
                }
                System.out.println();
                rowindex++;
            }
            return false;
        }catch (SQLException e){
            System.out.println("Ошибка синтаксиса. " + e);
            return false;
        }
    }


    /**
     * Экспортирует данные всех таблиц текущей схемы в отдельные Excel‑файлы формата XLSX.
     * <p>Каждая таблица сохраняется в файл с именем, совпадающим с именем таблицы.</p>
     */
    protected static void ExcelWriter() {
        try {
            Statement stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery("SELECT tablename FROM pg_tables WHERE schemaname = '" + schemaname+"'");
            Statement stmt2 = conn.createStatement();
            if (!rs.next()) {
                System.out.println("Создайте хотя бы одну таблицу! ");
                return;
            }
            rs = stmt.executeQuery("SELECT tablename FROM pg_tables WHERE schemaname = '" + schemaname + "'");
            while (rs.next()) {
                Workbook workbook = new XSSFWorkbook();
                String table = rs.getString(1);
                Sheet sheet = workbook.createSheet(table);
                ResultSet rs2 = stmt2.executeQuery("SELECT * FROM "+ schemaname +"." + table);
                ResultSetMetaData rsmd = rs2.getMetaData();
                int rowindex = 0;
                System.out.println(table);
                while (rs2.next()) {
                    Row row = sheet.createRow(rowindex);
                    for (int x = 1; x <= rsmd.getColumnCount(); x++)
                    {
                        if (rowindex == 0) {
                            row.createCell(x-1).setCellValue(rsmd.getColumnName(x));
                            System.out.printf("%-25s", rsmd.getColumnName(x));
                            if (x == rsmd.getColumnCount())
                            {
                                rowindex++;
                                x=1;
                                System.out.println();
                                row = sheet.createRow(rowindex);
                            } else continue;
                        }
                        TypeExtractor(row, rs2, x, rsmd.getColumnClassName(x));
                    }
                    System.out.println();
                    rowindex++;
                }
                if (sheet.getRow(0) != null) {
                    int columnCount = sheet.getRow(0).getPhysicalNumberOfCells();
                    for (int i = 0; i < columnCount; i++) {
                        sheet.autoSizeColumn(i);
                    }
                }
                workbook.write(new FileOutputStream(table + ".xlsx"));
                System.out.println("Данные успешно экспортированы в Excel-файл " + table + ".xlsx");
                workbook.close();

            }
        }
        catch (SQLException e){
        System.out.println("Выбранной таблицы не существует ошибка синтаксиса. " + e);
        } catch (IOException e){
            System.out.println("Информацию не удалось экспортировать. " + e);
        }
    }


   /**
    * Считывает значение из {@link ResultSet} в зависимости от типа столбца и
    * одновременно выводит его в консоль. При наличии объекта {@link Row} также
    * записывает значение в соответствующую ячейку Excel‑файла.
    *
    * @param row       строка Excel‑файла или {@code null}, если экспорт в Excel не требуется
    * @param rs        результат SQL‑запроса
    * @param x         индекс столбца (нумерация начинается с 1)
    * @param classname имя класса Java‑типа столбца (из {@link java.sql.ResultSetMetaData})
    * @throws SQLException при ошибке доступа к данным результата
    */
   private static void TypeExtractor(Row row, ResultSet rs, int x , String classname) throws SQLException {
       if (classname.equals("java.lang.Integer") || classname.equals("java.lang.Short") || classname.equals("java.lang.Long")) {
           if (row != null) {
               row.createCell(x - 1).setCellValue(rs.getLong(x));
           }
           System.out.printf("%-25d", rs.getInt(x));
       } else if (classname.equals("java.lang.String")) {
           if (row != null) {
               row.createCell(x-1).setCellValue(rs.getString(x));
           }
           if (rs.getString(x) != null && rs.getString(x).length() > 25){
               System.out.printf("%-25s", rs.getString(x).substring(0, 25) + "...");
           } else {
               System.out.printf("%-25s", rs.getString(x));
           }
       } else if (classname.equals("java.lang.Float")) {
           if (row != null) {
               row.createCell(x-1).setCellValue(rs.getFloat(x));
           }
           System.out.printf("%-25.2f", rs.getFloat(x));
       } else if (classname.equals("java.lang.Double")){
           if (row != null) {
               row.createCell(x-1).setCellValue(rs.getDouble(x));
           }
           if (rs.getDouble(x) < 100000000) System.out.printf("%-25.0f", rs.getDouble(x));
           else System.out.printf("%-25e", rs.getDouble(x));
       } else {
           if (row != null) {
               row.createCell(x-1).setCellValue("err");
           }
           System.out.printf("%-25s", "err");
       }
   }



}
