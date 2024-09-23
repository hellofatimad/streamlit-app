import streamlit as st
conn = st.connection("snowflake")


def create_table():
	try:
		with conn.cursor() as c:
			c.execute('CREATE TABLE IF NOT EXISTS taskstable(task TEXT,task_status TEXT,task_due_date DATE)')
			conn._instance.commit()
	except Exception as e:
		st.error(f"An error occurred: {e}")
        

def add_data(task,task_status,task_due_date):
	try:
		task = task.strip('"')
		with conn.cursor() as c:
			c.execute('INSERT INTO taskstable(task,task_status,task_due_date) VALUES (?,?,?)',(task,task_status,task_due_date))
			conn._instance.commit()
	except Exception as e:
		st.error(f"An error occurred: {e}")

def view_all_data():
	try:
		with conn.cursor() as c:
			c.execute('SELECT * FROM taskstable')
			conn._instance.commit()
			data = c.fetchall()
			return data
	except Exception as e:
		st.error(f"An error occurred: {e}")

def view_all_task_names():
	try:
		with conn.cursor() as c:
			c.execute('SELECT DISTINCT task FROM taskstable')
			conn._instance.commit()
			data = c.fetchall()
			return data
	except Exception as e:
		st.error(f"An error occurred: {e}")

def get_task(task):
	try:
		with conn.cursor() as c:
			c.execute('SELECT * FROM taskstable WHERE task= ?',(task,))
			conn._instance.commit()
			data = c.fetchall()
			return data
	except Exception as e:
		st.error(f"An error occurred: {e}")

def get_task_by_status(task_status):
	try:
		with conn.cursor() as c:
			c.execute('SELECT * FROM taskstable WHERE task_status=?',(task_status,))
			conn._instance.commit()
			data = c.fetchall()
			#return data
	except Exception as e:
		st.error(f"An error occurred: {e}")

def edit_task_data(new_task,new_task_status,new_task_date,task,task_status,task_due_date):
	try:
		with conn.cursor() as c:
			c.execute("UPDATE taskstable SET task =?,task_status=?,task_due_date=? WHERE task=? and task_status=? and task_due_date=? ",
			 (new_task,new_task_status,new_task_date,task,task_status,task_due_date))
			conn._instance.commit()
			data = c.fetchall()
			return data
	except Exception as e:
		st.error(f"An error occurred: {e}")


def delete_data(task):
	try:
		with conn.cursor() as c:
			c.execute('DELETE FROM taskstable WHERE task=?',(task,))
			conn._instance.commit()
	except Exception as e:
		st.error(f"An error occurred: {e}")
	