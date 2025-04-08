package org.example;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.ss.usermodel.Workbook;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;

import java.io.FileOutputStream;
import java.io.IOException;
import java.sql.*;

class SQLManager {
    protected static Connection conn;
    protected static final String schemaname = "task11";
    static {
        try {

            String pass = "9052";
            String user = "postgres";
            String url = "jdbc:postgresql://localhost:5432/test";
            conn = DriverManager.getConnection(url, user, pass);
            Statement stmt = conn.createStatement();
            stmt.executeUpdate("CREATE SCHEMA IF NOT EXISTS " + schemaname);
            System.out.println("База данных подключена. Выбранная схема: " + schemaname);
        } catch (SQLException e) {
            System.out.println("Не удалось подключиться к базе данных! " + e);
            System.exit(0);
        }
    }

    protected static void SQLQueryCreate(String query) {
        try {
            Statement stmt = conn.createStatement();
            int rowsAffected = stmt.executeUpdate(query);
            System.out.println("Данные успешно сохранены");
        } catch (SQLException e) {
            System.out.println("Ошибка при выполнении запроса: " + e.getMessage());
            System.out.println("Проблемный запрос: " + query);
        }
    }

    private static ResultSet SQLSelectAllTable(){
        try {
            Statement stmt = conn.createStatement();
            return stmt.executeQuery("SELECT tablename FROM pg_tables WHERE schemaname = '" + schemaname + "'");
        }catch (SQLException e){
            return null;
        }
    }

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
       } else if (classname.equals("java.lang.Double") || classname.equals("java.lang.Float")) {
           if (row != null) {
               row.createCell(x-1).setCellValue(rs.getDouble(x));
           }
           System.out.printf("%-25f", rs.getDouble(x));
       } else {
           if (row != null) {
               row.createCell(x-1).setCellValue("err");
           }
           System.out.printf("%-25s", "err");
       }
   }



}
