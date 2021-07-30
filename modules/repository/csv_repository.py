import os, os.path
import csv
from modules.repository.repository import Repository
from config.directory_config import DIR_REPORTS
from io import StringIO

class CsvRepository(Repository):
	def __init__(self, fields):
		super().__init__()
		self.fields = fields

	def get_last_product(self, product_id):
		header_string = ','.join(self.fields)
		filename = self.make_file_name(product_id)
		last_product_price = StringIO(header_string + '\n' + self.get_csv_last_line(filename))
		reader = csv.DictReader(last_product_price, delimiter=',')
		last_product=None
		for last_product in reader:
				pass
		return last_product

	def get_csv_last_line(self, filename):
		try:
			with open(filename, 'rb') as f:
				f.seek(-2, os.SEEK_END)
				while f.read(1) != b'\n':
					f.seek(-2, os.SEEK_CUR) 
				return f.readline().decode()
		except Exception as e:
			print(e)
			return ''

	def make_file_name(self, product_id):
		return f'{DIR_REPORTS}/{product_id}.csv'

	def append_product(self, product):
		filename = self.make_file_name(product["asin"])
		self.up(filename)
		with open(filename, 'a', newline='') as f:
			writer = csv.DictWriter(f, fieldnames=self.fields)
			writer.writerow(product)

	def up(self, filename):
		if not os.path.isfile(filename):
			with open(filename, 'w', newline='') as f:
				csv.DictWriter(f, self.fields).writeheader()