#!python3
#encoding:utf-8
import subprocess
import shlex
import Data
import time
import pytz
import requests
import json
import datetime

class Command:
    def __init__(self, data):
        self.data = data

    def CreateRepository(self):
        self.__CreateLocalRepository()
        r = self.__CreateRemoteRepository()
        self.__InsertRemoteRepository(r)
    def AddCommitPush(self, commit_message):
        """
        subprocess.call("git add .".format(commit_message).split(" "))
        subprocess.call("git commit -m '{0}'".format(commit_message).split(" "))
        subprocess.call("git push origin master".split(" "))
        """
        subprocess.call(shlex.split("git add ."))
        subprocess.call(shlex.split("git commit -m '{0}'".format(commit_message)))
        subprocess.call(shlex.split("git push origin master"))
        self.__InsertLanguages()

    def __CreateLocalRepository(self):
        subprocess.call(shlex.split("git init"))
        subprocess.call(shlex.split("git config --local user.name '{0}'".format(self.data.get_username())))
        subprocess.call(shlex.split("git config --local user.email '{0}'".format(self.data.get_mail_address())))
        subprocess.call(shlex.split("git remote add origin git@{0}:{1}/{2}.git".format(self.data.get_ssh_host(), self.data.get_username(), self.data.get_repo_name())))
        """
        subprocess.call("git init".split(" "))
        subprocess.call("git config --local user.name '{0}'".format(self.data.get_username()).split(" "))
        subprocess.call("git config --local user.email '{0}'".format(self.data.get_mail_address()).split(" "))
        subprocess.call("git remote add origin git@{0}:{1}/{2}.git".format(self.data.get_ssh_host(), self.data.get_username(), self.data.get_repo_name()))
        """

    def __CreateRemoteRepository(self):
        url = 'https://api.github.com/user/repos'
        post_data = json.dumps({"name": self.data.get_repo_name(), "description": self.data.get_repo_description(), "homepage": self.data.get_repo_homepage()})
        header_timezone = "Time-Zone: Asia/Tokyo"
        header_author = "Authorization: token {0}".format(self.data.get_access_token())
        json_file = "GitHub.{0}.{1}.js".format(self.data.get_username(), self.data.get_repo_name())
        command = "curl -k -o '{0}' -H '{1}' -H '{2}' {3} -d '{4}'".format(json_file, header_timezone, header_author, url, post_data)
#        res = subprocess.check_output(shlex.split(command))
        time.sleep(2)
        with open(json_file, 'r') as response:
            res = response.read()
            print(res)
            return json.loads(res)
        """
        POST_DATA='{"name":"'${REPO_NAME}'","description":"'${REPO_DESC}'","homepage":"'${REPO_HOME}'"}'
        echo ${POST_DATA}
        HDR_TIMEZONE="Time-Zone: Asia/Tokyo"
        HDR_AUTHOR="Authorization: token ${TOKEN}"
        JSON_FILE="GitHub.${USER_NAME}.${REPO_NAME}.json"
        curl -k  -o "${JSON_FILE}" -H "${HDR_TIMEZONE}" -H "${HDR_AUTHOR}" https://api.github.com/user/repos -d "${POST_DATA}"
        """

    def __InsertRemoteRepository(self, r):
        self.data.db_repo.begin()
        """
        self.data.db_repo['Repositories'].insert(dict(
            IdOnGitHub=r.id,
            Name=c,
            Description=r.description,
            Homepage=r.homepage,
            CreatedAt=r.created_at,
            PushedAt=r.pushed_at,
            UpdatedAt=r.updated_at,
            CheckedAt="{0:%Y-%m-%dT%H:%M:%SZ}".format(datetime.datetime.now(pytz.utc))
        ))
        self.data.db_repo['Counts'].insert(dict(
            RepositoryId=self.data.db_repo['Repositories'].find_one(Name=r.name)['Id'],
            Forks=r.forks_count,
            Stargazers=r.stargazers_count,
            Watchers=r.watchers_count,
            Issues=r.open_issues_count
        ))
        """
        self.data.db_repo['Repositories'].insert(dict(
            IdOnGitHub=r['id'],
            Name=r['name'],
            Description=r['description'],
            Homepage=r['homepage'],
            CreatedAt=r['created_at'],
            PushedAt=r['pushed_at'],
            UpdatedAt=r['updated_at'],
            CheckedAt="{0:%Y-%m-%dT%H:%M:%SZ}".format(datetime.datetime.now(pytz.utc))
        ))
        self.data.db_repo['Counts'].insert(dict(
            RepositoryId=self.data.db_repo['Repositories'].find_one(Name=r['name'])['Id'],
            Forks=r['forks_count'],
            Stargazers=r['stargazers_count'],
            Watchers=r['watchers_count'],
            Issues=r['open_issues_count']
        ))
        self.data.db_repo.commit()

#        sql = "INSERT INTO Repositories(IdOnGitHub,Name,Description,Homepage,CreatedAt,PushedAt,UpdatedAt,CheckedAt) VALUES({0}, '{1}','{2}','{3}','{4}','{5}','{6}','{7}');".format(r.id, r.name, r.description, r.homepage, r.created_at, r.pushed_at, r.updated_at, "{0:%Y-%m-%dT%H:%M:%SZ}".format(datetime.datetime.now(pytz.utc)))
        """
        local SQL="INSERT INTO Repositories(IdOnGitHub,Name,Description,Homepage,CreatedAt,PushedAt,UpdatedAt,CheckedAt) VALUES(${IdOnGitHub},'${Name}','${Description}','${Homepage}','${CreatedAt}','${PushedAt}','${UpdatedAt}','${CheckedAt}');"
        local COMMAND="sqlite3 ${DB_REPO}"
        echo $SQL | $COMMAND
        """

    def __InsertLanguages(self):
        url = 'https://api.github.com/repos/{0}/{1}/languages'.format(self.data.get_username(), self.data.get_repo_name())
        r = requests.get(url)
        if 300 <= r.status_code:
            print(r.status_code)
            print(r.text)
            raise Exception("HTTP Error {0}".format(r.status_code))
            return None

        self.data.db_repo.begin()
        repo_id = self.data.db_repo['Repositories'].find_one(Name=self.data.get_repo_name())['Id']
        self.data.db_repo['Languages'].delete(RepositoryId=repo_id)
        res = json.loads(r.text)
        for key in res.keys():
            self.data.db_repo['Languages'].insert(dict(
                RepositoryId=repo_id,
                Language=key,
                Size=res[key]
            ))
        self.data.db_repo.commit()
        """
        method = 'GET'
        endpoint = 'repos/:owner/:repo/languages'
        params = self.req.get(method, endpoint)
        endpoint = 'repos/{0}/{1}/languages'.format(self.req.get_username(), repo_name)
        r = requests.get(urllib.parse.urljoin("https://api.github.com", endpoint), **params)
        if 300 <= r.status_code:
            print(r.status_code)
            print(r.text)
            raise Exception("HTTP Error {0}".format(r.status_code))
            return None
        else:
            return json.loads(r.text)
        """

