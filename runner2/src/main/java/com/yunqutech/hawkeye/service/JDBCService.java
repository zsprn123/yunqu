package com.yunqutech.hawkeye.service;

import java.util.List;
import java.util.Map;

/**
 * Created by wangkai on 2017/10/17.
 */

public interface JDBCService {

    List<Map<String, Object>> query(String JDBC_DRIVER, String DB_URL, String USER, String PASS, String SQL, String DB_NAME) throws Exception;

    Map<String, List<Map<String, Object>>> batch_query(String JDBC_DRIVER, String DB_URL, String USER, String PASS, Map<String, String> SQL, String DB_NAME) throws Exception;

    Map<String, String> exec_plsql(String JDBC_DRIVER, String DB_URL, String USER, String PASS, String SQL) throws Exception;

    Boolean testConnection(String JDBC_DRIVER, String DB_URL, String USER, String PASS) throws Exception;

    Map<String, List<Map<String, Object>>> batch_rule_query(String JDBC_DRIVER, String DB_URL, String USER, String PASS, String SQL_TEXT, Map<String, String> SQL) throws Exception;

    List<Map<String, Object>> db2_plan_query(String JDBC_DRIVER, String DB_URL, String USER, String PASS, String SQL, String Schema) throws Exception;

    List<Map<String, Object>> mysql_plan_query(String JDBC_DRIVER, String DB_URL, String USER, String PASS, String SQL, String Schema) throws Exception;

    void closeConnection(String JDBC_DRIVER, String DB_URL, String USER, String PASS) throws Exception;

}
