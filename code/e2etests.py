from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import random

class ChessverseE2ETest(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    
    def test_login_happyPath(self):
        #checks if when the user logs in with correct credentials he is redirected to the options page
        self.driver.get('https://www.chessverse.cloud/login') 
        
        wait = WebDriverWait(self.driver, 10)
        #check if all elements are present
        username = wait.until(EC.presence_of_element_located((By.NAME, 'username')))
        password = wait.until(EC.presence_of_element_located((By.NAME, 'password')))
        submit = wait.until(EC.presence_of_element_located((By.ID, 'buttonSubmit')))
        
        username.send_keys('ccirone')
        password.send_keys('Ciao1234!')
        submit.click()
        
        wait.until(EC.url_changes(self.driver.current_url))
        self.assertEqual(self.driver.current_url, 'https://www.chessverse.cloud/options')
    
    def test_login_wrongCredentials(self):
        #checks if when the user logs in with wrong credentials he is redirected to the login page
        self.driver.get('https://www.chessverse.cloud/login') 
        
        wait = WebDriverWait(self.driver, 10)
        #check if all elements are present
        username = wait.until(EC.presence_of_element_located((By.NAME, 'username')))
        password = wait.until(EC.presence_of_element_located((By.NAME, 'password')))
        submit = wait.until(EC.presence_of_element_located((By.ID, 'buttonSubmit')))
        
        username.send_keys('provaErrore')
        password.send_keys('provaErrore1')
        submit.click()
        
        self.assertEqual(self.driver.current_url, 'https://www.chessverse.cloud/login')
       

    def test_signup_happyPath(self):
        #generate a random nickname to avoid conflicts with other users
        nickname = 'prova' + str(random.randint(0, 1000000))
        #checks if when the user signs up with correct credentials he is redirected to the login page
        self.driver.get('https://www.chessverse.cloud/signup') 
        
        wait = WebDriverWait(self.driver, 10)
        #check if all elements are present
        username = wait.until(EC.presence_of_element_located((By.NAME, 'username')))
        password = wait.until(EC.presence_of_element_located((By.NAME, 'password')))
        eloSelect = wait.until(EC.presence_of_element_located((By.ID, 'elo')))
        submit = wait.until(EC.presence_of_element_located((By.ID, 'buttonSubmit')))
        
        #check if with all correct credentials the user is redirected to the login page
        username.send_keys(nickname)
        password.send_keys('Prova1!')
        eloSelect.send_keys('400')
        submit.click()
        
        wait.until(EC.url_changes(self.driver.current_url))
        self.assertEqual(self.driver.current_url, 'https://www.chessverse.cloud/login')
        
    def test_signup_wrongCredentials(self):
        #generate a random nickname to avoid conflicts with other users
        nickname = 'prova' + str(random.randint(0, 1000000))
        #checks if when the user signs up with wrong credentials he is redirected to the signup page
        self.driver.get('https://www.chessverse.cloud/signup') 
        
        wait = WebDriverWait(self.driver, 10)
        #check if all elements are present
        username = wait.until(EC.presence_of_element_located((By.NAME, 'username')))
        password = wait.until(EC.presence_of_element_located((By.NAME, 'password')))
        eloSelect = wait.until(EC.presence_of_element_located((By.ID, 'elo')))
        submit = wait.until(EC.presence_of_element_located((By.ID, 'buttonSubmit')))
        
        #check if with a nickname already taken the user isn't signed up
        username.send_keys('ccirone')
        password.send_keys('Ciao1234!')
        eloSelect.send_keys('400')
        submit.click()
        self.assertEqual(self.driver.current_url, 'https://www.chessverse.cloud/signup')
        
        #check if with a password that doesn't respect the requirements the user isn't signed up
        username.send_keys(nickname)
        password.send_keys('prova')
        eloSelect.send_keys('400')
        submit.click()
        self.assertEqual(self.driver.current_url, 'https://www.chessverse.cloud/signup')
        
        #check if with an elo that doesn't respect the requirements the user isn't signed up
        username.send_keys(nickname)
        password.send_keys('Prova1!')
        eloSelect.send_keys('1000')
        submit.click()
        self.assertEqual(self.driver.current_url, 'https://www.chessverse.cloud/signup')
        
    
 
if __name__ == "__main__":
    unittest.main()