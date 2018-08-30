package com.yunqutech.hawkeye;

import com.yunqutech.hawkeye.service.JDBCService;
import com.zaxxer.hikari.HikariDataSource;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.jdbc.DataSourceBuilder;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import javax.naming.Context;
import javax.naming.InitialContext;
import javax.naming.NamingException;
import javax.sql.DataSource;
import java.sql.*;
import java.util.*;

@RestController
@SpringBootApplication
public class NewApplication {

    @Autowired
    private JDBCService jdbcService;

    @RequestMapping("/exec")
    public List<Map<String, Object>> exec(@RequestBody Map<String, Object> payload) throws Exception {
        String JDBC_DRIVER = (String) payload.get("driver");
        String DB_URL = (String) payload.get("jdbc_url");
        String USER = (String) payload.get("user");
        String PASS = (String) payload.get("password");
        String SQL = (String) payload.get("sql");
        String DB_NAME = (String) payload.get("db_name");
        List<Map<String, Object>> resultList = jdbcService.query(JDBC_DRIVER, DB_URL, USER, PASS, SQL, DB_NAME);
        return resultList;
    }

    @RequestMapping("/exec_plsql")
    public Map<String, String> exec_plsql(@RequestBody Map<String, Object> payload) throws Exception {
        String JDBC_DRIVER = (String) payload.get("driver");
        String DB_URL = (String) payload.get("jdbc_url");
        String USER = (String) payload.get("user");
        String PASS = (String) payload.get("password");
        String SQL = (String) payload.get("sql");
        Map<String, String> result = jdbcService.exec_plsql(JDBC_DRIVER, DB_URL, USER, PASS, SQL);
        return result;
    }

    @RequestMapping("/batch_exec")
    public Map<String, List<Map<String, Object>>> batch_exec(@RequestBody Map<String, Object> payload) throws Exception {
        String JDBC_DRIVER = (String) payload.get("driver");
        String DB_URL = (String) payload.get("jdbc_url");
        String USER = (String) payload.get("user");
        String PASS = (String) payload.get("password");
        Map SQL = (Map) payload.get("sql");
        String DB_NAME = (String) payload.get("db_name");
        Map<String, List<Map<String, Object>>> result = jdbcService.batch_query(JDBC_DRIVER, DB_URL, USER, PASS, SQL, DB_NAME);
        return result;
    }

    @RequestMapping("/batch_rule_exec")
    public Map<String, List<Map<String, Object>>> batch_rule_exec(@RequestBody Map<String, Object> payload) throws Exception {
        String JDBC_DRIVER = (String) payload.get("driver");
        String DB_URL = (String) payload.get("jdbc_url");
        String USER = (String) payload.get("user");
        String PASS = (String) payload.get("password");
        String SQL_TEXT = (String) payload.get("sql_text");
        Map SQL = (Map) payload.get("sql");
        Map<String, List<Map<String, Object>>> result = jdbcService.batch_rule_query(JDBC_DRIVER, DB_URL, USER, PASS, SQL_TEXT, SQL);
        return result;
    }

    @RequestMapping("/get_sql_plan")
    public List<Map<String, Object>> db2_plan_exec(@RequestBody Map<String, Object> payload) throws Exception {
        String JDBC_DRIVER = (String) payload.get("driver");
        String DB_URL = (String) payload.get("jdbc_url");
        String USER = (String) payload.get("user");
        String PASS = (String) payload.get("password");
        String SQL = (String) payload.get("sql_text");
        String Schema = (String) payload.get("schema");
        String db_type = (String) payload.get("db_type");

        List<Map<String, Object>> result = Collections.EMPTY_LIST;
        if (db_type.equals("db2"))
            result = jdbcService.db2_plan_query(JDBC_DRIVER, DB_URL, USER, PASS, SQL, Schema);
        else if (db_type.equals("mysql"))
            result = jdbcService.mysql_plan_query(JDBC_DRIVER, DB_URL, USER, PASS, SQL, Schema);
        return result;
    }

    @RequestMapping("/test-conn")
    public Map<String, Boolean> testConn(@RequestBody Map<String, Object> payload) throws Exception {
        String JDBC_DRIVER = (String) payload.get("driver");
        String DB_URL = (String) payload.get("jdbc_url");
        String USER = (String) payload.get("user");
        String PASS = (String) payload.get("password");
        boolean result = jdbcService.testConnection(JDBC_DRIVER, DB_URL, USER, PASS);
        Map<String, Boolean> resultMap = new HashMap<>();
        resultMap.put("message", result);
        return resultMap;
    }

    @RequestMapping("/close-conn")
    public Map<String, String> closeConn(@RequestBody Map<String, Object> payload) throws Exception {
        String JDBC_DRIVER = (String) payload.get("driver");
        String DB_URL = (String) payload.get("jdbc_url");
        String USER = (String) payload.get("user");
        String PASS = (String) payload.get("password");
        jdbcService.closeConnection(JDBC_DRIVER, DB_URL, USER, PASS);
        Map<String, String> resultMap = new HashMap<>();
        resultMap.put("message", "关闭成功");
        return resultMap;
    }

    public static void main(String[] args) {
        SpringApplication.run(NewApplication.class, args);
    }

}
