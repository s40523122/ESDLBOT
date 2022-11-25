import os
import psycopg2

DATABASE_URL = {"database":"esdldb", "user":"esdl", "password":"bj/6m06",
                "host":"192.168.1.110", "port":"5432"}		# sql 資訊

class mySQL:
	def __init__(self, table_name):
		self.table_name = table_name

	# 建立 sql 表單
	def creat_sql(self, table_items):
		# table_item = ("ItemA", "ItemB":, "ItemC")
		try:
			conn = psycopg2.connect(**DATABASE_URL, sslmode='require')							# 連接 Postgresql
			cursor = conn.cursor()
			
			type_dict = {"1":"text", "2":"real", "3":"integer"}
			
			items_msg = ""
			
			for item in table_items:
				type_no = input(f'''Input the type of {item} in number. (1:text, 2:real, 3:integer) : ''')
				items_msg += f''', {item} {type_dict[type_no]}'''

			cursor.execute(f'''CREATE TABLE {self.table_name}({items_msg[2:]});''')							# 執行 SQL
			conn.commit()
			print("The table has creat successfully !")
		except Exception as e:
			print(e)
			print("The table name isn't exist !")
			return "error"
		finally:
			cursor.close()
			conn.close()

	# 刪除 sql 表單
	def bye_sql(self):
		try:
			conn = psycopg2.connect(**DATABASE_URL, sslmode='require')							# 連接 Postgresql
			cursor = conn.cursor()
			cursor.execute(f'''DROP TABLE IF EXISTS {self.table_name}''')							# 執行 SQL
			conn.commit()
			print(f"""The table "{self.table_name}" was murdered by you !!!""")
		except Exception as e:
			print(e)
			print("The table doesn't delete !")
		finally:
			cursor.close()
			conn.close()

	# Change type of sql 表單欄位
	def retype_sql_column(self, column_name):
		try:
			conn = psycopg2.connect(**DATABASE_URL, sslmode='require')							# 連接 Postgresql
			cursor = conn.cursor()
			type_dict = {"1":"text", "2":"real", "3":"integer"}
			type_no = input(f'''Input the type of {column_name} in number. (1:text, 2:real, 3:integer) : ''')
			cursor.execute(f'''ALTER TABLE {self.table_name} ALTER COLUMN {column_name} TYPE {type_dict[type_no]};''')		# 執行 SQL
			conn.commit()
			print(f"""The column {column_name} retype successfully !!!""")
		except Exception as e:
			print(e)
			print("The column doesn't retype !")
		finally:
			cursor.close()
			conn.close()
	
	# 新增 sql 表單欄位
	def new_sql_column(self, column_name):
		try:
			conn = psycopg2.connect(**DATABASE_URL, sslmode='require')							# 連接 Postgresql
			cursor = conn.cursor()
			type_dict = {"1":"text", "2":"real", "3":"integer"}
			type_no = input(f'''Input the type of {column_name} in number. (1:text, 2:real, 3:integer) : ''')
			cursor.execute(f'''ALTER TABLE {self.table_name} ADD COLUMN {column_name} {type_dict[type_no]};''')		# 執行 SQL
			conn.commit()
			print(f"""The column "{column_name}" add successfully !!!""")
		except Exception as e:
			print(e)
			print("The column doesn't add !")
		finally:
			cursor.close()
			conn.close()
			
	# 刪除 sql 表單欄位
	def del_sql_column(self, column_name):
		'''
		To delete an old column for table.
		'''
		try:
			conn = psycopg2.connect(**DATABASE_URL, sslmode='require')							# 連接 Postgresql
			cursor = conn.cursor()
			cursor.execute(f'''ALTER TABLE {self.table_name} DROP COLUMN {column_name};''')		# 執行 SQL
			conn.commit()
			print(f"""Bye~ "{column_name}"!!!""")
		except Exception as e:
			print(e)
			print("The column doesn't delete !")
		finally:
			cursor.close()
			conn.close()


	# 變更 sql 欄位名稱
	def rename_sql_column(self, old_name, new_name):
		try:
			conn = psycopg2.connect(**DATABASE_URL, sslmode='require')							# 連接 Postgresql
			cursor = conn.cursor()
			cursor.execute(f'''ALTER TABLE {self.table_name} RENAME COLUMN {old_name} TO {new_name};''')			# 執行 SQL
			conn.commit()
			print(f"""The column name has been changed !!!""")
		except Exception as e:
			print(e)
			print("The column name doesn't change !")
		finally:
			cursor.close()
			conn.close()

	# 讀取 sql 中每一列之值 並以 list 返回
	def read_sql(self):
		try:
			conn = psycopg2.connect(**DATABASE_URL, sslmode='require')							# 連接 Postgresql
			cursor = conn.cursor()
		
			cursor.execute(f"""SELECT column_name, data_type FROM information_schema.columns WHERE table_name = '{self.table_name}';""")
			columns = cursor.fetchall()
			colname = [column[0] for column in columns]
			coltype = [column[1] for column in columns]
			colnamet = colname.copy()
			for i in range(len(colname)):
				if len(colname[i]) < 8:
					colnamet[i] = colname[i] + '\t'
			#print(*colnamet, sep='\t')
			#print(*coltype, sep='\t\t')
			#print("=====================")
			cursor.execute(f"""select * from {self.table_name} ORDER BY record_no ASC""")
			#row_cnt = cursor.rowcount															# 計算總列數
			#row = cursor.fetchmany(row_cnt1)														# 所有列值以 list 紀錄
			row = cursor.fetchall()
			#print(row, "\n=============================")
			return colname, row
		except Exception as e:
			print(e)
			print("The table name isn't exist !")
			return "error"
		finally:
			cursor.close()
			conn.close()

	# 新增資料至 sql 中
	def add_sql(self, add_items):
		#########################################################
		# table_columns = (ItemA, ItemB, ItemC) 		  #
		# add_items = ["18:00", "這則訊息永遠不會出現"]	  #
		#########################################################
		try:
			table_list = self.read_sql()
			print(table_list)
			table_list[1][0]
			lastColumns = table_list[1][-1]												# 取得最後一列資料
		except Exception as e:
			lastColumns = [0]
		try:
			conn = psycopg2.connect(**DATABASE_URL, sslmode='require')							# 連接 Postgresql
			cursor = conn.cursor()
			add_items.insert(0, lastColumns[0] + 1)												# 將 record_no 加入列表
			values = ",".join(["%s"] * len(add_items))
			table_items_txt = "(" + ", ".join(table_list[0]) + ")"
			postgres_insert_query = f"""INSERT INTO {self.table_name} {table_items_txt} VALUES ({values})"""
			cursor.execute(postgres_insert_query, add_items)
			conn.commit()
			count = cursor.rowcount
			print(count, "Record inserted successfully into table")
		except Exception as e:
			print(e)
			print("Record inserted error")
			return "error"
		finally:
			cursor.close()
			conn.close()

	# 更新 sql 資料
	def update_sql(self, item, no, value):
		# 刪除
		try:
			conn = psycopg2.connect(**DATABASE_URL, sslmode='require')							# 連接 Postgresql
			cursor = conn.cursor()
			sql_update_query = f"""Update {self.table_name} set {item} = {value} where record_no = {no}"""
			cursor.execute(sql_update_query)
			conn.commit()
			count = cursor.rowcount
			print(count, "Record Update successfully into table")
		except Exception as e:
			print("Record update error")
			return "error"
		finally:
			cursor.close()
			conn.close()

	# 刪除 sql 中指定一列
	def del_sql(self, no):
		# 刪除
		try: 
			conn = psycopg2.connect(**DATABASE_URL, sslmode='require')							# 連接 Postgresql
			cursor = conn.cursor()
			cursor.execute(f"""DELETE FROM {self.table_name} WHERE record_no = {no}""")
			conn.commit()
			count = cursor.rowcount
			print(count, "Record successfully delete from table")
			# 將序號重新編排
			row_no = [x[0] for x in self.read_sql()[1]]										# 取得舊序號
			#print(row_no)
			# 取代舊序號
			for i in range(1, len(row_no)+1):
				sql_update_query = f"""Update {self.table_name} set record_no = %s where record_no = %s"""
				cursor.execute(sql_update_query, (i, row_no[i-1]))
				conn.commit()
			print("序號重新編排成功 !")
		except Exception as e:
			print(e)
			return "error"
		finally:
			cursor.close()
			conn.close()
	


#### test ######## test  ######## test ######## test ######## test ######## test ######## test ########
if __name__ == '__main__':
	def main():
		'''
		sche = 'Schedule'
		columns = '(record_no, sche_time, sche_work)'
		test_columns = '(record_no, sche_time, sche_work)'
		dicc = {"record_no":"integer", "sche_time":"text", "sche_work":"text"}
		aaa = {"record_no":"integer", "ID":"text", "total":"integer", "fifty":"integer", "ten":"integer", "five":"integer", "one":"integer"}
		'''
		
		#sql = mySQL("car_sensor")
		sql = mySQL("maps")
		
		## Delete specify row ##
		#sql.del_sql(1)
		
		## Create new table ##
		table_item = ("record_no", "names")
		#sql.creat_sql(table_item)
		
		## Add new data ##
		msg = ["turtle_house_gmapping"]
		#sql.add_sql(msg)
		
		## Delete table ##
		#sql.bye_sql()
		
		## Retype the type of item ##
		#sql.retype_sql_column('area')
		
		## Add new item ##
		#sql.new_sql_column("Humidity")	
		#sql.new_sql_column("CO2")	
		#sql.new_sql_column("Time")
			
		## Delete item ##
		#sql.del_sql_column("ItemB")
		
		## Change item name ##
		#sql.rename_sql_column("demo", "Area")
		#sql.rename_sql_column("demo2", "Temperture")
		
		## Udate values ##
		#sql.update_sql("demo", 1, 3)
		
		## Read all table ##
		print(sql.read_sql())
		#import time
		#conn = psycopg2.connect(**DATABASE_URL, sslmode='require')							# 連接 Postgresql
		#cursor = conn.cursor()
		#while 1:
		#	cursor.execute(f'''Select * FROM car_sensor LIMIT 0''')
		#	colnames = [desc[0] for desc in cursor.description]
		#	print(colnames)										# 所有列值以 list 紀錄
		#	time.sleep(1)


#### test ######## test  ######## test ######## test ######## test ######## test ######## test ########

	main()
