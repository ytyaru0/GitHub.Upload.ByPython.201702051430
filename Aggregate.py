#!python3
#encoding:utf-8
from datetime import datetime
class Aggregate:
    def __init__(self, data):
        self.data = data
        self.__first_date = None
        self.__last_date = None
        self.__date_span = None
        self.__date_format = "%Y-%m-%dT%H:%M:%SZ"
        self.__sum_code_size = 0

    def Show(self):
        self.__calc_date()
        print("開始日: " + self.__date_format.format(self.__first_date))
        print("最終日: " + self.__date_format.format(self.__last_date))
        print("期  間: " + self.__date_span + " 日間")
        print("リポジトリ総数  : " + self.data.db_repo['Repositories'].count())
        print("リポジトリ平均数: " + self.data.db_repo['Repositories'].count() / self.__date_span + " repo/日")

        self.__sum_code_size = self.data.db_repo.query("select SUM(Size) SumSize from Languages;")['SumSize']
        print("コード: " + self.__sum_code_size + " Byte")
        self.__show_sizes_by_languages()

    def __calc_date(self):
        first_date = self.data.db_repo.query("select min(CreatedAt) FirstDate from Repositories;").next()['FirstDate']
        last_date = self.data.db_repo.query("select max(CreatedAt) LastDate from Repositories;").next()['LastDate']
        self.__first_date = datetime.strptime(first_date, self.__date_format)
        self.__last_date = datetime.strptime(last_date, self.__date_format)
        self.__date_span = (self.__last_date - self.__first_date).days
        
    """
    def __show_code(self):
        self.__sum_code_size = self.data.db_repo.query("select SUM(Size) SumSize from Languages;")['SumSize']
        print("コード: " + self.__sum_code_size + " Byte")
        self.__sum_langs_code_size = "select Language,SUM(Size) SumSize from Languages group by Language order by SumSize desc;"
        for lang in self.__sum_langs_code_size:
            print("{0}{1}".format(lang['Language'], lang['SumSize']))
    """

    def __show_sizes_by_languages(self):
        # 桁あわせ：最も長い言語名を取得する
        name_length = 0
        for res in self.db_repo.query('select * from Languages where length(Language)=(select max(length(Language)) from Languages)'):
            name_length = res['Language']

        # 桁あわせ：最も大きい言語別合計Byteを取得する
        size_length = self.db_repo.query('select sum(Size) SumSize from Languages group by Language order by SumSize desc').next()['SumSize']

        # 言語別の合計Byte数
        format_str = "  {0:<%d}: {1:>%d} Byte" % (len(name_length), len(str(size_length)))
        for lang in self.db_repo.query('select Language, sum(Size) SumSize from Languages group by Language order by SumSize desc'):
            print(format_str.format(lang['Language'], lang['SumSize']))

"""
function Aggregate()
{
    local COMMAND="sqlite3 ${DB_REPO}"
    local SQL="select count(*) RepoNum from Repositories;"
    local REPO_NUM=`echo $SQL | $COMMAND`
    echo "リポジトリ数: ${REPO_NUM}"

    local SQL="select min(CreatedAt) FirstDate from Repositories;"
    local FIRST_DATE=`echo $SQL | $COMMAND`
    echo "開始日: ${FIRST_DATE}"
    local SQL="select max(CreatedAt) LastDate from Repositories;"
    local LAST_DATE=`echo $SQL | $COMMAND`
    echo "終了日: ${LAST_DATE}"

    local FIRST_DATE_EPOC=`date -d"${FIRST_DATE}" +%s`
    local LAST_DATE_EPOC=`date -d"${LAST_DATE}" +%s`
    local DATE_SPAN=`expr \( ${LAST_DATE_EPOC} - ${FIRST_DATE_EPOC} \) / 60 / 60 / 24`
    echo "日数: ${DATE_SPAN} 日間"

    local AVG_REPO=`echo ${REPO_NUM} / ${DATE_SPAN} | awk '{print $1 / $3}'`
    echo "平均: ${AVG_REPO} repo/日"

    # 総Byte数
    local SQL="select SUM(Size) SumSize from Languages;"
    local SUM_SIZE=`echo $SQL | $COMMAND`
    echo "合計: ${SUM_SIZE} Byte"
    local AVG_SIZE=`echo ${SUM_SIZE} / ${DATE_SPAN} | awk '{print $1 / $3}'`
    echo "平均: ${AVG_SIZE} Byte"

    # 言語別Byte数
    local SQL="select Language,SUM(Size) SumSize from Languages group by Language order by SumSize desc;"
    echo $SQL | $COMMAND
}
"""

