#!python3
#encoding:utf-8
import os.path
import subprocess
from configparser import ConfigParser, ExtendedInterpolation
import dataset

class Data:
    def __init__(self):
        self.file_path_config = './config.ini'
        self.config = ConfigParser(interpolation=ExtendedInterpolation())
        self.config.read(self.file_path_config)
        self.db_acc = dataset.connect('sqlite:///' + self.config['SQLite']['Accounts'])
        self.db_repo = dataset.connect('sqlite:///' + self.config['SQLite']['Repositories'])
    def initialize(self):
        if not(os.path.exists(self.file_path_config)):
            with open(self.file_path_config, 'w', encoding='UTF-8') as conf:
                conf.write('[GitHub]')
                conf.write('Username=user1')
                conf.write('[SSH]')
                conf.write('# ~/.ssh/confファイルの')
                conf.write('Host=github.com.$(GitHub:Username)')
                conf.write('[SQLite]')
                conf.write('Accounts=./GitHub.Accounts.sqlite3')
                conf.write('Repositories=./GitHub.Repositories.$(GitHub:Username).sqlite3')
                conf.write('[Repository]')
                conf.write('Description=リポジトリ説明。')
                conf.write('Homepage=http://')
            print("'{0}'ファイルを作成しました。任意に編集してからやり直してください。ファイルの各値は'{1}'ファイルを参考にしてください。".format(self.file_path_config, 'config.ini.help.md'))

    def get_username(self):
        return self.config['GitHub']['Username']
    def get_ssh_host(self):
        return self.config['SSH']['Host']
    def get_mail_address(self):
        return self.db_acc['Accounts'].find_one(Username=self.get_username())['MailAddress']
    def get_access_token(self, scopes=None):
        sql = "SELECT * FROM AccessTokens WHERE AccountId == {0}".format(self.db_acc['Accounts'].find_one(Username=self.get_username())['Id'])
        if not(None is scopes):
            sql = sql + " AND ("
            for s in scopes:
                sql = sql + "(',' || Scopes || ',') LIKE '%,{0},%'".format(s) + " OR "
            sql = sql.rstrip(" OR ")
            sql = sql + ')'
        return self.db_acc.query(sql).next()['AccessToken']
    def get_repo_name(self):
        return os.path.basename(os.path.dirname(os.path.abspath(__file__)))
    def get_repo_description(self):
        return self.config['Repository']['Description']
    def get_repo_homepage(self):
        return self.config['Repository']['Homepage']

