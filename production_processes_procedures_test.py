#!/usr/bin/python
# coding=utf8

import unittest
from selenium import webdriver

class Three_Pi(unittest.TestCase):
    # ЖСК
    JSK = 'http://suok.ezeev.ru/llc/'

    # Выбираем нужный фильтр для отображения производств
    RADIO_PROCEEDINGS = '//*[@id="control"]//div[2]/div[1]/div[1]/label'
    # Ищем нужный файл производства
    PROCEEDINGS_FILE = u'Открыть карточку производства'

    # Выбираем фильтр для отображения процессов
    RADIO_PROCESSES = '//*[@id="control"]//div[2]/div[1]/div[2]/label'
    # Ищем нужный файл процесса
    PROCESSES_FILE = u'Открыть карточку процесса'

    # Выбираем фильтр для отображения процедур
    RADIO_PROCEDURES = '//*[@id="control"]//div[2]/div[1]/div[3]/label'
    # Ищем нужный файл процедуры
    PROCEDURES_FILE = u'Открыть карточку процедуры'

    # Архивация
    IN_ARCHIVE = u'В архив'
    # Восстановление из архива
    RETURN_FROM_ARCHIVE = u'Восстановить из архива'

    # Закрываем процесс
    CLOSE_PROCEEDING = u'Закрыть производство'
    # Вновь открываем процесс
    REOPEN_PROCEEDING = u'Переоткрыть производство'

    # Закрываем процесс
    CLOSE_PROCESS = u'Закрыть процесс'
    # Вновь открываем процесс
    REOPEN_PROCESS = u'Переоткрыть процесс'

    # Закрытие процедуры
    CLOSE_PROCEDURE = u'Закрыть процедуру'
    # Переоткрытие процедуры
    REOPEN_PROCEDURE = u'Переоткрыть процедуру'

    # открываем браузер, переходим на страницу
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.driver.maximize_window()
        self.driver.get('http://suok.ezeev.ru/llc/#')
        # Login
        login = '******@gmail.com'
        password = '******'
        # Вводим данные для входа
        self.driver.find_element_by_id('employee_email').send_keys(login)
        self.driver.find_element_by_id('employee_password').send_keys(password)
        self.driver.find_element_by_xpath("//button[@type='submit']").submit()

    def Preparing(self, detalization, open_file):
        i = 1
        self.driver.get(self.JSK)
        assert 'ЖСК' in self.driver.title
        self.driver.find_element_by_xpath(detalization).click()
        assert 'ЖСК' in self.driver.title
        while True:
            original_title = self.driver.find_element_by_xpath('//*[@id="batch-operations-form"]//tr[{0}]/td[3]/a[3]'\
                                                               .format(i)).get_attribute('data-original-title')
            if original_title == open_file:
                self.driver.find_element_by_xpath('//*[@id="batch-operations-form"]//tr[{0}]/td[3]/a[3]'\
                                                  .format(i)).click()
                # Архивация процесса
                self.Archivation(self.IN_ARCHIVE)
                return False
            i += 1

    def Archivation(self, archive):
        self.driver.find_element_by_partial_link_text(archive).click()
        try:
            self.driver.switch_to.alert.accept()
        except:
            pass

    def Close_smth(self, close_param):
        self.driver.find_element_by_partial_link_text(close_param).click()
        try:
            self.driver.switch_to.alert.accept()
        except:
            pass

    # Тест производств
    def test_proceedings(self):
        self.Preparing(self.RADIO_PROCEEDINGS, self.PROCEEDINGS_FILE )
        # Проверка успешности архивации
        self.assertEqual('ЖСК', self.driver.title)
        # Восстановление и проверка успешности этого действия
        self.Archivation(self.RETURN_FROM_ARCHIVE)
        self.assertEqual('ЖСК', self.driver.title)
        # Закрываем производство
        self.Close_smth(self.CLOSE_PROCEEDING)
        self.assertEqual('ЖСК', self.driver.title)
        # Открываем производство вновь
        self.Close_smth(self.REOPEN_PROCEEDING)
        self.assertEqual('ЖСК', self.driver.title)

    # Тест процессов
    def test_processes(self):
        self.Preparing(self.RADIO_PROCESSES, self.PROCESSES_FILE)
        # Проверка успешности завершения архивации
        self.assertEqual('ЖСК', self.driver.title)
        # Проверка успешности восстановления процесса из архива
        self.Archivation(self.RETURN_FROM_ARCHIVE)
        self.assertEqual('ЖСК', self.driver.title)
        # Закрываем процесс
        self.Close_smth(self.CLOSE_PROCESS)
        self.assertEqual('ЖСК', self.driver.title)
        # Переоткрываем процесс
        self.Close_smth(self.REOPEN_PROCESS)
        self.assertEqual('ЖСК', self.driver.title)

    # Тест процедуры
    '''def test_procedures(self):
        self.Preparing(self.RADIO_PROCEDURES, self.PROCEDURES_FILE, self. PROCEDURES_OPEN)
        # Проверка успешности завершения архивации
        self.assertEqual('ЖСК', self.driver.title)
        # Проверка успешности восстановления процесса из архива
        self.Archivation(self.RETURN_FROM_ARCHIVE)
        self.assertEqual('ЖСК', self.driver.title)'''


    def tearDown(self):
        self.driver.quit()

if __name__ == '__main__':
    unittest.main()