package org.example;
import org.apache.poi.ss.usermodel.Row;
import org.apache.poi.ss.usermodel.Sheet;
import org.apache.poi.ss.usermodel.Workbook;
import org.apache.poi.xssf.usermodel.XSSFWorkbook;

import java.io.FileOutputStream;
import java.io.IOException;
import java.sql.*;

public class SQLManager {
    private static Connection conn;
    static {
        try {
            String pass = "postgres";
            String user = "postgres";
            String url = "jdbc:postgresql://localhost:5432/postgres";
            conn = DriverManager.getConnection(url, user, pass);
            Statement stmt = conn.createStatement();
            stmt.executeUpdate("CREATE SCHEMA IF NOT EXISTS Task5");
        } catch (SQLException e) {
            System.out.println("Не удалось подключиться к базе данных! " + e);
            System.exit(0);
        }
    }

    private static void SQLQueries(String query, String type) {
        try {
            Statement stmt = conn.createStatement();
            if (type.equals("select")) {
                ResultSet rs = stmt.executeQuery(query);
                while (rs.next()) {
                    System.out.println(rs.getString(1));
                }
            } else if (type.equals("create")) {
                stmt.executeUpdate(query);
            } else if (type.equals("excel")) {
                ResultSet rs = stmt.executeQuery(query);
                Statement stmt2 = conn.createStatement();
                while (rs.next()) {
                    Workbook workbook = new XSSFWorkbook();
                    String table = rs.getString(1);
                    Sheet sheet = workbook.createSheet(table);
                    ResultSet rs2 = stmt2.executeQuery("SELECT * FROM task5." + table);
                    ResultSetMetaData rsmd = rs2.getMetaData();
                    int rowindex = 0;
                    while (rs2.next()) {
                        Row row = sheet.createRow(rowindex);
                        for (int x = 1; x <= rsmd.getColumnCount(); x++)
                        {
                            if (rowindex == 0) {
                                row.createCell(x-1).setCellValue(rsmd.getColumnName(x));
                                System.out.printf("%-22s", rsmd.getColumnName(x));
                                if (x == rsmd.getColumnCount())
                                {
                                    rowindex++;
                                    x=1;
                                    System.out.println();
                                    row = sheet.createRow(rowindex);
                                } else continue;
                            }
                            if (rsmd.getColumnClassName(x).equals("java.lang.Integer") || rsmd.getColumnClassName(x).equals("java.lang.Short")) {
                                row.createCell(x-1).setCellValue(rs2.getInt(x));
                                System.out.printf("%-22d", rs2.getInt(x));
                            } else if (rsmd.getColumnClassName(x).equals("java.lang.String")) {
                                row.createCell(x-1).setCellValue(rs2.getString(x));
                                System.out.printf("%-22s", rs2.getString(x));
                            } else if (rsmd.getColumnClassName(x).equals("java.lang.Double") || rsmd.getColumnClassName(x).equals("java.lang.Float")) {
                                row.createCell(x-1).setCellValue(rs2.getDouble(x));
                                System.out.printf("%-22f", rs2.getDouble(x));
                            }
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

        } catch (SQLException e){
            System.out.println("Выбранной таблицы не существует ошибка синтаксиса. " + e);
        } catch (IOException e){
            System.out.println("Информацию не удалось экспортировать. " + e);
        }
    }

    private static void ExcelCreator(int i, ResultSet rs) throws SQLException {

    }

}
