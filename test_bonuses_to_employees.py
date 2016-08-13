#!/usr/bin/python
# coding=utf8

import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By

class BonusTest(unittest.TestCase):
	#Добавление новой премии
	NEW_BONUS = '/html/body/div[2]/ul/li[2]/a'
	#Список сотрудников
	LIST_OF_EMPLOYEES = '//*[@id="user_id-form-group"]/div/div/button'
	#Выобр "Езееф Ф.А." из всего списка работников
	WORKER = '//*[@id="user_id-form-group"]/div/div/div/ul/li[5]/a/span'
	#Кнопка "Далее"
	NEXT = '//*[@id="btn-submit-1"]'
	#Последняя созданная премия
	BONUS = '//div[2]/table/tbody/tr[1]/td/a'
	#Сумма начёта
	SUMM_OF_BONUS = 'additional_amount'
	#Комментарий к премии
	COMMENT = '//*[@id="comment"]'
	#Кнопка сохранений изменений в премии
	SAVE_EDITIONS = '//*[@id="btn-submit-1"]'
	#Archive
	IN_ARCHIVE = u'В архив'
	# Отрицательное значение для тестирования
	NEGATIVE_BONUS = -35
	#Отрицательное значение для редактирования старого
	NEGATIVE_BONUS_EDIT = -10
	#Переменная с дробной частью записанная через точку
	FRACTIONAL_NUMBER_DOT = '-18.25'
	#Переменная с дробной частью записанная через точку, для редактирования старой записи
	FRACTIONAL_NUMBER_DOT_EDIT = '-74.69'
	#Переменная с дробной частью записанная через точку
	FRACTIONAL_NUMBER_COMMA = '-11,50'
	##Переменная с дробной частью записанная через точку, для редактирования старой записи
	FRACTIONAL_NUMBER_COMMA_EDIT = '-37,98'


	# открываем браузер, переходим на страницу
	def setUp(self):
		self.driver = webdriver.Chrome()
		self.driver.implicitly_wait(30)
		self.driver.maximize_window()
		self.driver.get('http://suok.ezeev.ru/llc/#')
		#Login
		login = '****@gmail.com'
		password = '****'
		# Вводим данные для входа
		self.driver.find_element_by_id('employee_email').send_keys(login)
		self.driver.find_element_by_id('employee_password').send_keys(password)
		self.driver.find_element_by_xpath("//button[@type='submit']").submit()

	#Функция проверки налчичя не подписанной премии и её архивация
	def Checking(self):
		#Ожидание элемента
		self.driver.implicitly_wait( 0.5 )
		# Переходим в раздел под названием Suok
		self.driver.find_element_by_link_text( u"Suok" ).click( )
		assert u"Suok" in self.driver.title
		# Переход в раздел с премиями
		self.driver.find_element_by_link_text( u'Премии' ).click( )
		#Открываем форму с премией
		self.driver.find_element_by_xpath(self.BONUS).click()
		#Пытаемся отправить форму в архив
		try:
			# Архивация премии
			self.driver.find_element_by_partial_link_text( self.IN_ARCHIVE ).click()
			# Переключение на всплывающее окно  и подтверждение действия по архивации премии
			self.driver.switch_to.alert.accept()
		except:
			self.driver.back()


	def Bonus_Creating(self):
		#Переход  в раздел с добавлением новой премии сотруднику
		self.driver.find_element_by_xpath(self.NEW_BONUS).click()
		#Открытие списка работников
		self.driver.find_element_by_xpath(self.LIST_OF_EMPLOYEES).click()
		#Выбор нужного работника
		self.driver.find_element_by_xpath(self.WORKER).click()
		# Переход в форму для заполнения данных по выплатам
		self.driver.find_element_by_xpath(self.NEXT).click()
		assert u'Расчет премии' in self.driver.title

	#Заполнение полей данными
	def Bonus_Filling(self,variable):
		# Ввод нужных данных премии
		self.driver.find_element_by_id(self.SUMM_OF_BONUS).clear()
		self.driver.find_element_by_id(self.SUMM_OF_BONUS).send_keys(variable)
		# Ввод комментария
		self.driver.find_element_by_xpath(self.COMMENT).clear()
		self.driver.find_element_by_xpath(self.COMMENT).send_keys(u'-=Комментарий=-')
		# Сохранение изменение
		self.driver.find_element_by_xpath(self.SAVE_EDITIONS).click()

	#Отрицательное значение в сумму начета
	def test_negative_summ(self):
		self.Checking()
		self.Bonus_Creating()
		self.Bonus_Filling(self.NEGATIVE_BONUS)

		#Проверяем сохранилась ли преми и не появилось ли ошибок
		self.assertNotEqual(self.driver.title, u'Расчет премии')

		# Переход к ранее созданной премии
		self.driver.find_element_by_xpath(self.BONUS).click()
		#Извлечение значения строки с премией
		SUMM_AMOUNT = self.driver.find_element(By.ID, self.SUMM_OF_BONUS).get_attribute('value')
		#Извлечение целого значения
		SUMM_AMOUNT = SUMM_AMOUNT.split(',')
		SUMM_AMOUNT = int(SUMM_AMOUNT[0])

		#Проверка соответствия введённых ранее данных и того что сохранилось
		self.assertEqual(self.NEGATIVE_BONUS, SUMM_AMOUNT)

		#Ввод отрицательных данных
		self.Bonus_Filling(self.NEGATIVE_BONUS_EDIT)

		#Проверяем сохранилась ли преми и не появилось ли ошибок
		self.assertNotEqual(self.driver.title, u'Расчет премии')

		# Извлечение значения строки с премией
		SUMM_AMOUNT = self.driver.find_element(By.ID, self.SUMM_OF_BONUS).get_attribute('value')
		# Извлечение целого значения
		SUMM_AMOUNT = SUMM_AMOUNT.split(',')
		SUMM_AMOUNT = int(SUMM_AMOUNT[0])
		#Проверка соответствия введённых ранее данных и того что сохранилось
		self.assertEqual(self.NEGATIVE_BONUS_EDIT, SUMM_AMOUNT)

		#Архивация премии
		self.driver.find_element_by_partial_link_text(self.IN_ARCHIVE).click()
		#Переключение на всплывающее окно  и подтверждение действия по архивации премии
		self.driver.switch_to.alert.accept()

	#Проверка дробного числа записанного с точкой
	def test_fractional_number_dot(self):
		self.Checking( )
		self.Bonus_Creating()
		self.Bonus_Filling(self.FRACTIONAL_NUMBER_DOT)

		# Проверяем сохранилась ли преми и не появилось ли ошибок
		self.assertNotEqual(self.driver.title, u'Расчет премии')

		# Переход к ранее созданной премии
		self.driver.find_element_by_xpath(self.BONUS).click()
		# Извлечение значения строки с премией
		SUMM_AMOUNT = self.driver.find_element(By.ID, self.SUMM_OF_BONUS).get_attribute('value')
		#Преобразование строки с переменной в дробное число
		SUMM_AMOUNT = SUMM_AMOUNT.split(',')
		SUMM_AMOUNT = float(SUMM_AMOUNT[0]+'.'+SUMM_AMOUNT[1])
		#Преобразование начального значение(строкой) в дробную переменную
		self.FRACTIONAL_NUMBER_DOT = float(self.FRACTIONAL_NUMBER_DOT)

		#Проверка на равенство сохраненного значения и начальное переменной
		self.assertEqual(SUMM_AMOUNT, self.FRACTIONAL_NUMBER_DOT)

		self.Bonus_Filling(self.FRACTIONAL_NUMBER_DOT_EDIT)

		# Проверяем сохранилась ли преми и не появилось ли ошибок
		self.assertNotEqual(self.driver.title, u'Расчет премии')

		# Извлечение значения строки с премией
		SUMM_AMOUNT = self.driver.find_element(By.ID, self.SUMM_OF_BONUS).get_attribute('value')
		# Извлечение значения
		SUMM_AMOUNT = float(SUMM_AMOUNT)
		# Преобразование начального значение(строкой) в дробную переменную
		self.FRACTIONAL_NUMBER_DOT_EDIT = float(self.FRACTIONAL_NUMBER_DOT_EDIT)

		# Проверка соответствия введённых ранее данных и того что сохранилось
		self.assertEqual(SUMM_AMOUNT, self.FRACTIONAL_NUMBER_DOT_EDIT)
		# Архивация премии
		self.driver.find_element_by_partial_link_text(self.IN_ARCHIVE).click()
		# Переключение на всплывающее окно  и подтверждение действия по архивации премии
		self.driver.switch_to.alert.accept()

	#Проверка дробного числа записанного с запятой
	def test_fractional_number_comma(self):
		self.Checking( )
		self.Bonus_Creating()
		self.Bonus_Filling(self.FRACTIONAL_NUMBER_COMMA)

		# Проверяем сохранилась ли преми и не появилось ли ошибок
		self.assertNotEqual(self.driver.title, u'Расчет премии')

		# Переход к ранее созданной премии
		self.driver.find_element_by_xpath(self.BONUS).click()
		# Извлечение значения строки с премией
		SUMM_AMOUNT = self.driver.find_element(By.ID, self.SUMM_OF_BONUS).get_attribute('value')
		# Преобразование строки с переменной в дробное число
		SUMM_AMOUNT = SUMM_AMOUNT.split(',')
		SUMM_AMOUNT = float(SUMM_AMOUNT[0]+'.'+SUMM_AMOUNT[1])
		# Преобразование начального значение(строкой) в дробную переменную
		self.FRACTIONAL_NUMBER_COMMA = self.FRACTIONAL_NUMBER_COMMA.split(',')
		self.FRACTIONAL_NUMBER_COMMA = float(self.FRACTIONAL_NUMBER_COMMA[0]+'.'+ self.FRACTIONAL_NUMBER_COMMA[1])

		# Проверка на равенство сохраненного значения и начальное переменной
		self.assertEqual(SUMM_AMOUNT, self.FRACTIONAL_NUMBER_COMMA)

		self.Bonus_Filling(self.FRACTIONAL_NUMBER_COMMA_EDIT)
		# Проверяем сохранилась ли преми и не появилось ли ошибок
		self.assertNotEqual(self.driver.title, u'Расчет премии')

		# Извлечение значения строки с премией
		SUMM_AMOUNT = self.driver.find_element(By.ID, self.SUMM_OF_BONUS).get_attribute('value')
		# Извлечение целого значения
		SUMM_AMOUNT = SUMM_AMOUNT.split(',')
		SUMM_AMOUNT = float(SUMM_AMOUNT[0]+'.'+SUMM_AMOUNT[1])
		# Преобразование начального значение(строкой) в дробную переменную
		self.FRACTIONAL_NUMBER_COMMA_EDIT = self.FRACTIONAL_NUMBER_COMMA_EDIT.split(',')
		self.FRACTIONAL_NUMBER_COMMA_EDIT = float(self.FRACTIONAL_NUMBER_COMMA_EDIT[0]+'.'+ self.FRACTIONAL_NUMBER_COMMA_EDIT[1])

		# Проверка соответствия введённых ранее данных и того что сохранилось
		self.assertEqual(SUMM_AMOUNT, self.FRACTIONAL_NUMBER_COMMA_EDIT)

		# Архивация премии
		self.driver.find_element_by_partial_link_text(self.IN_ARCHIVE).click()
		# Переключение на всплывающее окно  и подтверждение действия по архивации премии
		self.driver.switch_to.alert.accept()

	def tearDown(self):
		self.driver.quit()

if __name__ == '__main__':
	unittest.main()
