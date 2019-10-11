package Core;

import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;

public class dbConnection {
	private String user = "";
	private String passwd = "";
	private String dbname = "";
	private String url = "";
	private Connection conn = null;
	
	public dbConnection() {
		user = "java1";
		passwd = "123456";
		dbname = "java_test";
		url = "jdbc:sqlserver://127.0.0.1:1433;" + "databaseName=" + dbname;
	}
	
	public dbConnection(String user, String passwd, String dbname) {
		this.user = user;
		this.passwd = passwd;
		this.dbname = dbname;
		url = "jdbc:sqlserver://127.0.0.1:1433;" + "databaseName=" + dbname;
	}
	
	public Connection openConnection() {
		try {
			if(conn == null || conn.isClosed()) {
				conn = DriverManager.getConnection(url, user, passwd);
			} 
		}
		catch (Exception e) {
			// TODO: handle exception
			e.printStackTrace();
		}
		return conn;
	}
	
	public ResultSet executeSelectQuery(String _query, String[] sqlParameter) {
		ResultSet rs = null;
		try {
			openConnection();
			PreparedStatement stmt = conn.prepareStatement(_query);
			for(int i=0;i<sqlParameter.length;i++) {
				stmt.setString(i+1, sqlParameter[i]);
			}
			rs = stmt.executeQuery();
			
		} catch (Exception e) {
			// TODO: handle exception
			System.out.println("Error - Connection.executeSelectQuery - Query: " + _query + " \nException: " + e.toString());
			return null;
		}
		return rs;
		
	}
	
	public Boolean executeInsertQuery(String _query, String[] sqlParameter) {
		try {
			openConnection();
			PreparedStatement stmt = conn.prepareCall(_query);
			for(int i=0;i<sqlParameter.length;i++) {
				stmt.setString(i+1, sqlParameter[i]);
			}
			stmt.executeUpdate();
			
		} catch (Exception e) {
			// TODO: handle exception
			System.out.println("Error - Connection.executeInsertQuery - Query: " + _query + " \nException: " + e.toString());
			return false;
		}
		return true;
	}
	
	public Boolean executeUpdateQuery(String _query, String[] sqlParameter) {
		try {
			openConnection();
			PreparedStatement stmt = conn.prepareCall(_query);
			for(int i=0;i<sqlParameter.length;i++) {
				stmt.setString(i+1, sqlParameter[i]);
			}
			stmt.executeUpdate();
			
		} catch (Exception e) {
			// TODO: handle exception
			System.out.println("Error - Connection.executeUpdateQuery - Query: " + _query + " \nException: " + e.toString());
			return false;
		}
		return true;
	}
	
	public void test(String query) {
		ResultSet rs = null;
		try {
			openConnection();
			PreparedStatement stmt = conn.prepareStatement(query);
			rs = stmt.executeQuery();
			while (rs.next()) {
				System.out.println(rs.getString("fname"));
			}
		} catch (Exception e) {
			// TODO: handle exception
			System.out.println("Error - Connection.executeSelectQuery - Query: " + query + " \nException: " + e.toString());
		}
	}
}
