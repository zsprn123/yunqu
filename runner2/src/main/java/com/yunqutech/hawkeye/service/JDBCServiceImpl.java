package com.yunqutech.hawkeye.service;

import com.zaxxer.hikari.HikariDataSource;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.autoconfigure.jdbc.DataSourceBuilder;
import org.springframework.context.annotation.PropertySource;
import org.springframework.context.annotation.Scope;
import org.springframework.jdbc.support.JdbcUtils;
import org.springframework.stereotype.Component;
import org.springframework.stereotype.Service;
import org.springframework.util.CollectionUtils;
import org.springframework.util.LinkedCaseInsensitiveMap;

import javax.sql.DataSource;
import java.beans.Transient;
import java.io.IOException;
import java.net.ConnectException;
import java.sql.*;
import java.util.*;

/**
 * Created by wangkai on 2017/10/17.
 */

@Service
@Scope("prototype")
public class JDBCServiceImpl implements JDBCService {

    public static Map<String, HikariDataSource> DataSourcePool = new HashMap();

    @Value("${datasource_login_timeout:2000}")
    private int LOGIN_TIMEOUT;

    @Value("${datasource_maxconn:10}")
    private int MAX_CONNECTIONS;


    private void createDatabaseSource(String JDBC_DRIVER, String DB_URL, String USER, String PASS) {
        HikariDataSource ds = new HikariDataSource();
        ds.setMaximumPoolSize(MAX_CONNECTIONS);
//        ds.setLeakDetectionThreshold(5000);
        ds.setJdbcUrl(DB_URL);
        ds.setUsername(USER);
        ds.setDriverClassName(JDBC_DRIVER);
        ds.setPassword(PASS);
        ds.setConnectionTimeout(LOGIN_TIMEOUT);
        DataSourcePool.put(DB_URL + USER + PASS, ds);
    }

    public List<Map<String, Object>> query(String JDBC_DRIVER, String DB_URL, String USER, String PASS, String SQL, String DB_NAME) throws Exception {
        Connection conn = null;
        Statement stmt = null;
        List<Map<String, Object>> resultList = Collections.EMPTY_LIST;
        try {
            Class.forName(JDBC_DRIVER);
            String datasourseKey = DB_URL + USER + PASS;
            if (!DataSourcePool.containsKey(datasourseKey)) {
                createDatabaseSource(JDBC_DRIVER, DB_URL, USER, PASS);
            }
            String schema_sql = "use ";
            HikariDataSource ds = DataSourcePool.get(datasourseKey);
            conn = ds.getConnection();
            stmt = conn.createStatement();

            stmt = conn.createStatement();
            if (DB_NAME != null && !DB_NAME.isEmpty()) {
                schema_sql = schema_sql + DB_NAME;
                stmt.execute(schema_sql);
            }
            ResultSet rs = stmt.executeQuery(SQL);
            resultList = getResultLlist(rs);
            rs.close();
        } catch (SQLException e) {
            System.out.println(SQL);
            e.printStackTrace();
            throw e;
        } finally {
            try {
                if (stmt != null) {
                    stmt.close();
                }
                if (conn != null) {
                    conn.close();
                }
            } catch (SQLException se) {
                se.printStackTrace();
            }
        }
        return resultList;
    }

    public Map<String, String> exec_plsql(String JDBC_DRIVER, String DB_URL, String USER, String PASS, String SQL) throws Exception {
        Connection conn = null;
        Statement stmt = null;
        Map<String, String> result = new HashMap();
        try {
            Class.forName(JDBC_DRIVER);
            String datasourseKey = DB_URL + USER + PASS;
            if (!DataSourcePool.containsKey(datasourseKey)) {
                createDatabaseSource(JDBC_DRIVER, DB_URL, USER, PASS);
            }
            HikariDataSource ds = DataSourcePool.get(datasourseKey);
            conn = ds.getConnection();
            stmt = conn.createStatement();
            stmt.execute(SQL);
            result.put("OK", "true");
            return result;
        } catch (SQLException e) {
            System.out.println(SQL);
            e.printStackTrace();
            throw e;
        } finally {
            try {
                if (stmt != null) {
                    stmt.close();
                }
                if (conn != null) {
                    conn.close();
                }
            } catch (SQLException se) {
                se.printStackTrace();
            }
        }
    }


    @Override
    @Transient
    public Map<String, List<Map<String, Object>>> batch_query(String JDBC_DRIVER, String DB_URL, String USER, String PASS, Map<String, String> SQL, String DB_NAME) throws Exception {
        Connection conn = null;
        Statement stmt = null;
        int a = 1;
        Map<String, List<Map<String, Object>>> resultMap = new HashMap();
        try {
            Class.forName(JDBC_DRIVER);
            String datasourseKey = DB_URL + USER + PASS;
            if (!DataSourcePool.containsKey(datasourseKey)) {
                createDatabaseSource(JDBC_DRIVER, DB_URL, USER, PASS);
            }
            HikariDataSource ds = DataSourcePool.get(datasourseKey);
            conn = ds.getConnection();
            stmt = conn.createStatement();
            String schema_sql = "use ";

            if (DB_NAME != null && !DB_NAME.isEmpty()) {
                schema_sql = schema_sql + DB_NAME;
                stmt.execute(schema_sql);
            }

            int idx = 0;
            Statement finalStmt = stmt;
            SQL.forEach((k, v) -> {
                try {
                    List<Map<String, Object>> resultList;
                    ResultSet rs = null;
                    rs = finalStmt.executeQuery((String) v);
                    resultList = getResultLlist(rs);
                    rs.close();
                    resultMap.put(k, resultList);
                } catch (SQLException e) {
                    System.out.println((String) v);
                    e.printStackTrace();
                } catch (Exception e) {
                    e.printStackTrace();
                }
            });
        } finally {
            try {
                if (stmt != null) {
                    stmt.close();
                }
                if (conn != null) {
                    conn.close();
                }
            } catch (SQLException se) {
                se.printStackTrace();
            }
        }
        return resultMap;
    }

    @Override
    @Transient
    public Map<String, List<Map<String, Object>>> batch_rule_query(String JDBC_DRIVER, String DB_URL, String USER, String PASS, String SQL_TEXT, Map<String, String> SQL) throws Exception {
        Connection conn = null;
        Statement stmt = null;
        int a = 1;
        Map<String, List<Map<String, Object>>> resultMap = new HashMap();
        try {
            Class.forName(JDBC_DRIVER);
            String datasourseKey = DB_URL + USER + PASS;
            if (!DataSourcePool.containsKey(datasourseKey)) {
                createDatabaseSource(JDBC_DRIVER, DB_URL, USER, PASS);
            }
            HikariDataSource ds = DataSourcePool.get(datasourseKey);
            conn = ds.getConnection();
            String delete_sql = "delete from plan_table";
            String explain_sql = "explain plan for " + SQL_TEXT;

            stmt = conn.createStatement();
            stmt.execute(delete_sql);
            stmt.execute(explain_sql);
            int idx = 0;
            Statement finalStmt = stmt;
            SQL.forEach((k, v) -> {
                try {
                    List<Map<String, Object>> resultList;
                    ResultSet rs = null;
                    rs = finalStmt.executeQuery((String) v);
                    resultList = getResultLlist(rs);
                    rs.close();
                    resultMap.put(k, resultList);
                } catch (SQLException e) {
                    System.out.println((String) v);
                    e.printStackTrace();
                } catch (Exception e) {
                    System.out.println((String) v);
                    e.printStackTrace();
                }
            });
        } finally {
            try {
                if (stmt != null) {
                    stmt.close();
                }
                if (conn != null) {
                    conn.close();
                }
            } catch (SQLException se) {
                se.printStackTrace();
            }
        }
        return resultMap;
    }

    @Override
    public Boolean testConnection(String JDBC_DRIVER, String DB_URL, String USER, String PASS) throws Exception{

        try {
            Class.forName(JDBC_DRIVER);
            Connection conn = DriverManager.getConnection(DB_URL, USER, PASS);
            if (conn != null) {
                conn.close();
                return Boolean.TRUE;
            }
        } catch (ClassNotFoundException e) {
            e.printStackTrace();
        } catch (SQLException e) {
            String datasourseKey = DB_URL + USER + PASS;
            closeDataSource(datasourseKey);
            e.printStackTrace();
            throw e;
            //return Boolean.FALSE;
        }
        return Boolean.FALSE;
    }

    @Override
    public void closeConnection(String JDBC_DRIVER, String DB_URL, String USER, String PASS) throws Exception{
        String datasourseKey = DB_URL + USER + PASS;
        closeDataSource(datasourseKey);
        return ;
    }

    private static List<Map<String, Object>> getResultLlist(ResultSet rs) throws Exception {
        List<Map<String, Object>> resultList = new ArrayList();
        while (rs.next()) {
            ResultSetMetaData rsmd = rs.getMetaData();
            int columnCount = rsmd.getColumnCount();
            Map<String, Object> mapOfColValues = new LinkedCaseInsensitiveMap<Object>(columnCount);
            for (int i = 1; i <= columnCount; i++) {
                String key = JdbcUtils.lookupColumnName(rsmd, i);
                Object obj = JdbcUtils.getResultSetValue(rs, i);
                mapOfColValues.put(key, obj);
            }
            resultList.add(mapOfColValues);
        }
        return resultList;
    }

    public List<Map<String, Object>> db2_plan_query(String JDBC_DRIVER, String DB_URL, String USER, String PASS, String SQL, String Schema) throws Exception {
        Connection conn = null;
        Statement stmt = null;
        List<Map<String, Object>> resultList = Collections.EMPTY_LIST;
        try {
            Class.forName(JDBC_DRIVER);
            String datasourseKey = DB_URL + USER + PASS;
            if (!DataSourcePool.containsKey(datasourseKey)) {
                createDatabaseSource(JDBC_DRIVER, DB_URL, USER, PASS);
            }
            HikariDataSource ds = DataSourcePool.get(datasourseKey);
            conn = ds.getConnection();
            String delete_sql = "delete from EXPLAIN_INSTANCE";
            String schema_sql = "set schema " + Schema;
            String explain_sql = "explain plan for " + SQL;
            String plan_sql = " WITH tree(operator_ID, level, Operator_Type, previous_Operator_Type, explain_time, Cost)" +
                    " AS" +
                    " (" +
                    "   SELECT" +
                    "     1                             operator_id," +
                    "     0                             level," +
                    "     O.Operator_Type," +
                    "     '' previous_Operator_Type," +
                    "     O.explain_time                explain_time," +
                    "     CAST(O.Total_Cost AS INTEGER) Cost" +
                    "   FROM EXPLAIN_OPERATOR O" +
                    "   WHERE O.operator_id = 1" +
                    "   UNION ALL" +
                    "   SELECT" +
                    "     o.operator_id ," +
                    "     level + 1," +
                    "     O.Operator_Type," +
                    "     tree.Operator_Type previous_Operator_Type," +
                    "     O.explain_time                explain_time," +
                    "     CAST(O.Total_Cost AS INTEGER) Cost" +
                    "   FROM tree" +
                    "     , EXPLAIN_STREAM S" +
                    "     , EXPLAIN_OPERATOR O" +
                    "   WHERE s.target_id = tree.operator_id" +
                    "         AND s.source_id = o.operator_id" +
                    "         AND s.explain_time = tree.explain_time" +
                    " )" +
                    " select" +
                    "   O.Operator_ID ID, lpad(' ', o.level*2,' ')||O.Operator_Type  PLAN_STEP, O.Operator_Type, o.previous_Operator_Type, s.STREAM_COUNT CARDINALITY, rtrim(s.OBJECT_SCHEMA) Object_OWNER, S.Object_Name, O.Cost," +
                    "   (select SUBSTR(XMLCAST(XMLGROUP(' AND ' || predicate_text AS a)" +
                    "                  AS VARCHAR(200)), 6) predicate_text from explain_predicate p1 where p1.Operator_ID = O.Operator_ID and rtrim(how_applied) in ('START', 'STOP', 'SARG') group by p1.Operator_ID) ACCESS_PREDICATES," +
                    "   (select SUBSTR(XMLCAST(XMLGROUP(' AND ' || predicate_text AS a)" +
                    "                  AS VARCHAR(200)), 6) predicate_text from explain_predicate p1 where p1.Operator_ID = O.Operator_ID and rtrim(how_applied) not in ('START','STOP', 'SARG') group by p1.Operator_ID ) FILTER_PREDICATES" +
                    " from tree o" +
                    " LEFT OUTER JOIN EXPLAIN_STREAM S" +
                    " ON O.Operator_ID = S.Target_ID" +
                    " AND O.Explain_Time = S.Explain_Time" +
                    " AND S.Object_Name IS NOT NULL" +
                    " order by operator_ID";

            stmt = conn.createStatement();
            try {
                try {
                    stmt.execute(schema_sql);
                    stmt.execute(delete_sql);
                } catch (SQLException e) {
                    String new_schema_sql = "set schema " + "SYSTOOLS";
                    stmt.execute(new_schema_sql);
                    stmt.execute(delete_sql);
                }
            } catch (SQLException e) {
                e.printStackTrace();
            }

            stmt.execute(schema_sql);

            stmt.execute(explain_sql);
            try {
                ResultSet rs = stmt.executeQuery(plan_sql);
                resultList = getResultLlist(rs);
                stmt.execute(delete_sql);
                stmt.execute("COMMIT");
                rs.close();
            } catch (SQLException e) {
                schema_sql = "set schema " + "SYSTOOLS";
                stmt.execute(schema_sql);
                ResultSet rs = stmt.executeQuery(plan_sql);
                resultList = getResultLlist(rs);
                stmt.execute(delete_sql);
                stmt.execute("COMMIT");
                rs.close();
            }
        } catch (SQLException e) {
            System.out.println(SQL);
            e.printStackTrace();
            throw e;
        } finally {
            try {
                if (stmt != null) {
                    stmt.close();
                }
                if (conn != null) {
                    conn.close();
                }
            } catch (SQLException se) {
                se.printStackTrace();
            }
        }
        return resultList;
    }

    public List<Map<String, Object>> mysql_plan_query(String JDBC_DRIVER, String DB_URL, String USER, String PASS, String SQL, String Schema) throws Exception {
        Connection conn = null;
        Statement stmt = null;
        List<Map<String, Object>> resultList = Collections.EMPTY_LIST;
        try {
            Class.forName(JDBC_DRIVER);
            String datasourseKey = DB_URL + USER + PASS;
            if (!DataSourcePool.containsKey(datasourseKey)) {
                createDatabaseSource(JDBC_DRIVER, DB_URL, USER, PASS);
            }
            HikariDataSource ds = DataSourcePool.get(datasourseKey);
            conn = ds.getConnection();
            String schema_sql = "use " + Schema;
            String explain_sql = "explain " + SQL;

            stmt = conn.createStatement();
            stmt.execute(schema_sql);
            ResultSet rs = stmt.executeQuery(explain_sql);
            resultList = getResultLlist(rs);
            rs.close();
        } catch (SQLException e) {
            System.out.println(SQL);
            e.printStackTrace();
            throw e;
        } finally {
            try {
                if (stmt != null) {
                    stmt.close();
                }
                if (conn != null) {
                    conn.close();
                }
            } catch (SQLException se) {
                se.printStackTrace();
            }
        }
        return resultList;
    }

    private static void closeDataSource(String datasourseKey) {
        if (DataSourcePool.containsKey(datasourseKey)) {
            HikariDataSource ds = DataSourcePool.get(datasourseKey);
            ds.close();
            DataSourcePool.remove(datasourseKey);
        }
        return;
    }
}
