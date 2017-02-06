#!python3
#encoding:utf-8
import os.path
import subprocess
import Data
import Command
import Aggregate

class Main:
    def __init__(self):
        self.data = Data.Data()
        self.cmd = Command.Command(self.data)
        self.agg = Aggregate.Aggregate(self.data)

    def Run(self):
        if -1 != self.__Create():
            self.__Commit()

    def __CreateInfo(self):
        print('ユーザ名: ' + self.data.get_username())
        print('メアド: ' + self.data.get_mail_address())
        print('SSH HOST: ' + self.data.get_ssh_host())
        print('リポジトリ名: ' + self.data.get_repo_name())
        print('説明: ' + self.data.get_repo_description())
        print('URL: ' + self.data.get_repo_homepage())
        print('リポジトリ情報は上記のとおりで間違いありませんか？[y/n]')

    def __Create(self):
        if os.path.exists(".git"):
            return 0
        answer = ''
        while '' == answer:
            self.__CreateInfo()
            answer = input()
            if 'y' == answer or 'Y' == answer:
#                self.__CreateCommands()
                self.cmd.CreateRepository()
                return 0
            elif 'n' == answer or 'N' == answer:
                print('conf.iniを編集して再度やり直してください。')
                return -1
            else:
                answer = ''
    """
    def __CreateCommands(self):
        print('(ローカルリポジトリを作成する。)')
        subprocess.call("git init".format(commit_message).split(" "))
        subprocess.call("git config --local user.name '{0}'".format(self.data.get_username()).split(" "))
        subprocess.call("git config --local user.email '{0}'".format(self.data.get_mail_address()).split(" "))
        subprocess.call("git remote add origin git@{0}:{1}/{2}.git".format(self.data.get_ssh_host(),self.data.get_username(),self.data.get_repo_name()).split(" "))
        self.__CreateRemoteRepo()
        self.__InsertRemoteRepo()

    def __CreateRemoteRepo(self):
        print('(リモートリポジトリを作成する。(未実装))')

    def __InsertRemoteRepo(self):
        print('(ローカルDBにリモートリポジトリ情報を登録する。(未実装))')
    """

    def __CommitInfo(self):
        print('リポジトリ名： {0}/{1}'.format(self.data.get_username(), self.data.get_repo_name()))
        print('説明: ' + self.data.get_repo_description())
        print('URL: ' + self.data.get_repo_homepage())
        print('----------------------------------------')
        subprocess.call('git add -n .'.split(" "))
        print('commit,pushするならメッセージを入力してください。Enterかnで終了します。')
        print('サブコマンド    n:終了 e:編集 d:削除 i:Issue作成')

    def __Commit(self):
        self.__CommitInfo()
        answer = input()
        if '' == answer or 'n' == answer or 'N' == answer:
            print('何もせず終了します。')
        elif 'e' == answer or 'E' == answer:
            print('(リポジトリ編集する。(未実装))')
        elif 'd' == answer or 'D' == answer:
            print('(リポジトリ削除する。(未実装))')
        elif 'i' == answer or 'I' == answer:
            print('(Issue作成する。(未実装))')
        else:
            self.cmd.AddCommitPush(answer)
            self.agg.Show()
#            self.__CommitCommands(answer)
#            self.__Aggregate()

"""
    def __CommitCommands(self, commit_message):
        subprocess.call("git add .".format(commit_message).split(" "))
        subprocess.call("git commit -m '{0}'".format(commit_message).split(" "))
        subprocess.call("git push origin master".split(" "))

    def __Aggregate(self):
        print('(集計を表示する。(未実装))')
"""

if __name__ == "__main__":
    main = Main()
    main.Run()

