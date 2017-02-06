# config.iniファイル説明

## GitHub:Username

GitHubで[アカウント作成](https://github.com/join)したときのユーザ名を指定する。

ユーザ名が`user1`なら以下のようになる。

```ini
[GitHub]
Username=user1
```

## GitHub.Repository:Description

作成するリモートリポジトリの説明文を指定する。

```ini
[GitHub]
	[Repository]
	Description=リポジトリ説明。
```

## GitHub.Repository:Homepage

作成するリモートリポジトリの関連URLを指定する。

```ini
[GitHub]
	[Repository]
	Homepage=http://
```

## SSH:Host

```ini
[SSH]
Host=github.com.$(GitHub:Username)
```

`SSH.Host`にはGitHubアカウント用に作成したSSH鍵の`{OSユーザディレクトリ}/.ssh/config`ファイルで使用している`Host`名を指定する。

`git remote add origin git@${SSH_HOST}:${USER_NAME}/${REPO_NAME}.git`コマンドでリモートリポジトリとSSH通信するための設定をするために必要である。

### SSH設定ファイルについて

SSH鍵の作成とGitHubへの登録は[こちら](http://ytyaru.hatenablog.com/entry/2016/06/17/082230)を参考。

内容|パス
----|----
SSH設定|`.ssh/config`ファイル
SSH秘密鍵|`.ssh/rsa_{GitHub.Username}`ファイル
SSH公開鍵|`.ssh/rsa_{GitHub.Username}.pub`ファイル

`.ssh/config`ファイルは以下のような内容になる。

```
Host github.com.{GitHub.Username}
  User git
  Port 22
  HostName github.com
  IdentityFile ~/.ssh/rsa_{GitHub.Username}
  TCPKeepAlive yes
  IdentitiesOnly yes
```

このうち`Host github.com.{GitHub.Username}`の`Host `以降を`config.ini`ファイルの`SSH:Host`に指定する。

## SQLite:Accounts

SQLite3データベースファイルパスを指定する。

DBファイルは[Accounts](https://github.com/ytyaru/GitHub.Accounts.Database.20170107081237765)で作成する。データレコードは自分のアカウント情報を指定すること。

```ini
[SQLite]
Accounts="./GitHub.Accounts.sqlite3"
```

## SQLite:Repositories

SQLite3データベースファイルパスを指定する。

DBファイルは[Repositories](https://github.com/ytyaru/GitHub.Repositories.Database.Create.20170114123411296)で作成する。

```ini
[SQLite]
Repositories="./GitHub.Repositories.$(GitHub:Username).sqlite3"
```

