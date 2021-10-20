import sys
import sqlite3
#.......................
from datetime import datetime, date
dbName = "directiontechnique"
requestShowDb = "SHOW DATABASES"
requestShowTables = "SELECT name FROM sqlite_master WHERE type='table';"
tPlayer = "PLAYER"
tElo = "ELO"
tScore = "score"
tType = "tournamenttype"
tCategory = "category"
tTournament = "TOURNAMENT"
tRecompense = "recompense"
tPartie = "partie"
tJoueurTournoi = "JOUEURTOURNOI"
tExams = "EXAMS"
tExamsPlayer = "EXAMSPLAYER"
tSeance = "SESSION"
tSessionPlayer = "SESSIONPLAYER"
delTable = "DROP TABLE "
base = 'joueurbica.db'
Tpresence = "presence"
Tusers = "users"
Tpayment = "payment"
Tvip = "vip"

#.......................

class Mabase:
    def __init__(self, base):
        self.base = base
        self.mydb, self.mycursor, self.myresult = self.connect()
        #self.deleteTable(tScore)
        # self.deleteTable(tSessionPlayer)
        #self.deleteTable(Tusers)
        self.createAllTable()
        #Ãself.deletedata("score")
        #self.supprimer()
    #___________________
    def createAllTable(self):
        #self.deleteTable("PLAYER")
        self.createPlayerTable()
        self.createEloTable()
        self.createExamsTable()
        self.createExamsPlayerTable()
        self.createTournamentTable()
        self.createJoueurTournoiTable()
        self.createSessionTable()
        self.createSessionPlayerTable()
        self.createPresenceTable()
        self.createScoreTable()
        self.createUsersTable()
        
        self.createPaymentTable()
        
        self.createVipTable()
        
        # result = self.list_tables()
        # #print(self.mycursor,':',result)
    #___________________
    def connect(self):
        mydb = sqlite3.connect(self.base)
        mycursor = mydb.cursor()
        mycursor.execute(requestShowTables)
        myresult = mycursor.fetchall()
        ##print(mycursor,':',myresult)
        return mydb, mycursor, myresult

    #___________________
    def list_tables(self):
        self.mycursor.execute(requestShowTables)
        result = self.mycursor.fetchall()
        return result    
    #___________________
    def selectUser(self,n,p):
        self.mycursor = self.mydb.cursor()
        sql = "SELECT * FROM " + Tusers + " WHERE name='{}' and password='{}';".format(n,p)
        self.mycursor.execute(sql)
        result = self.mycursor.fetchone()
        self.mycursor.close()
        
        return result
    def selectAllUsers(self):
        self.mycursor = self.mydb.cursor()
        self.mycursor.execute("select * from users ")
        result = self.mycursor.fetchall()
        self.mycursor.close()
        return result

    def selectUserByName(self,n):
        self.mycursor = self.mydb.cursor()
        sql = "SELECT * FROM " + Tusers + " WHERE name='{}' ;".format(n)
        self.mycursor.execute(sql)
        result = self.mycursor.fetchone()
        self.mycursor.close()
        
        return result
    def selectNameUsers(self):
        self.mycursor = self.mydb.cursor()
        sql = "SELECT name FROM users" 
        self.mycursor.execute(sql)
        result = self.mycursor.fetchall()
        self.mycursor.close()
        
        return result

    def createUsersTable(self):
        sql ='''CREATE TABLE users(
            id INTEGER,
            name VARCHAR(30),
            password VARCHAR(50),
            view Integer,
            DAY DATE,
        PRIMARY KEY(`id`)
        )'''
        if ('users',) not in self.list_tables():
            self.mycursor.execute(sql)
        
            today = date.today()
            dayadd = today
            dayadd = date(2021,8,19)
            #dayadd = datetime.strptime(today, '%d/%m/%Y').date()
            records = [(1, 'Administrator', "BicaAdmin2021",1,dayadd),
                (2, 'Super User', "BicaSuser2021",2,dayadd),
                (3, 'Genior User', "BicaGenior2021",3,dayadd),
                (4, 'User', "",4,dayadd)]

    #insert multiple records in a single query
            self.mycursor.executemany('INSERT INTO users VALUES(?,?,?,?,?);',records);
            self.mydb.commit()
            ##print("data added OK : ", records)

    def insertUser(self,data):
        self.mycursor = self.mydb.cursor()
        self.mycursor.execute('INSERT INTO users VALUES(?,?,?,?,?);',data);
        self.mydb.commit()
        
    def updateUser(self,data):
        self.mycursor = self.mydb.cursor()
        
        self.mycursor.execute('UPDATE users SET name=?, password=?,view=?,DAY=? WHERE id = ?;',(data[1],data[2],data[3],data[4],data[0]))
        self.mydb.commit()
    def deleteUser(self,name):
        self.mycursor = self.mydb.cursor()
        self.mycursor.execute("DELETE FROM users WHERE name='{}';".format(name));
        self.mydb.commit()

    def createPaymentTable(self):
        sql ='''CREATE TABLE payment(
            j_id INTEGER,
            amount INTEGER,
            month INTEGER,
            day INTEGER,
            year INTEGER,
            
        CONSTRAINT `j_id` FOREIGN KEY (`j_id`) REFERENCES `player` (`id`) ON DELETE CASCADE,
        PRIMARY KEY(`j_id`,`month`,`year`)
        )'''
        if ('payment',) not in self.list_tables():
            self.mycursor.execute(sql)
            print(" payment  is created !")
        else:
            print('la table payment existe déjà dans la base!!!')
        
    def createVipTable(self):
        sql ='''CREATE TABLE vip(
            jo_id INTEGER,
            amount INTEGER,
            month INTEGER,
            year INTEGER,
            number INTEGER,
            
        CONSTRAINT `jo_id` FOREIGN KEY (`jo_id`) REFERENCES `player` (`id`) ON DELETE CASCADE,
        PRIMARY KEY(`jo_id`)
        )'''
        if ('vip',) not in self.list_tables():
            self.mycursor.execute(sql)
            print(" vip  is created !")
        else:
            print('la table vip existe déjà dans la base!!!')
        
    def createPlayerTable(self):
        sql ='''CREATE TABLE PLAYER(
                id INTEGER PRIMARY KEY,
                NAME VARCHAR(40) NOT NULL,
                sex VARCHAR(1),
                fed VARCHAR(10),
                clubnumber INTEGER,
                clubname VARCHAR(30),
                birthday DATE,
                GATEGORIE VARCHAR(20) NOT NULL,
                nelo INTEGER,
                fideno INTEGER,
                celo INTEGER,
                relo INTEGER,
                belo INTEGER,
                score INTEGER,
                title VARCHAR(10),
                k INTEGER,
                PICTURE VARCHAR(80),
                level INTEGER,
                phone INTEGER,
                mail VARCHAR(40),
                card VARCHAR(40)
                )'''
        if ('PLAYER',) not in self.list_tables():
            self.mycursor.execute(sql)
            ##print(" player table is created !")
        #else:
            ##print('la table player existe déjà dans la base!!!')
    #___________________
    def createEloTable(self):
        sql ='''CREATE TABLE ELO(
            player_id INTEGER,
            CLASSIC INTEGER,
            RAPID INTEGER,
            BLITZ INTEGER,
            NAT INTEGER,
            DAY DATE,
        CONSTRAINT `player_id` FOREIGN KEY (`player_id`) REFERENCES `player` (`id`) ON DELETE CASCADE,
        PRIMARY KEY(`player_id`,`DAY`)
        )'''
        if ('ELO',) not in self.list_tables():
            self.mycursor.execute(sql)
            ##print(" player elo is created !")
        #else:
            ##print('la table elo existe déjà dans la base!!!')
    #___________________

    def createScoreTable(self):
        sql ='''CREATE TABLE score(
            p_ids INTEGER,
            DAY DATE,
            levels INTEGER,
            score INTEGER,
            raison INTEGER,
        CONSTRAINT `p_ids` FOREIGN KEY (`p_ids`) REFERENCES `player` (`id`) ON DELETE CASCADE,
        PRIMARY KEY(`p_ids`,`DAY`,`raison`)
        )'''
        if ('score',) not in self.list_tables():
            self.mycursor.execute(sql)
            ##print(" score is created !")
        #else:
            ##print('la table score existe déjà dans la base!!!')
    #___________________


    def createExamsTable(self):
        sql ='''CREATE TABLE EXAMS(
        id INTEGER AUTO_INCREMENT PRIMARY KEY,
        NAMES VARCHAR(30),
        DATES DATE

        )'''
        if ('EXAMS',) not in self.list_tables():
            self.mycursor.execute(sql)
            ##print(" EXAMS elo is created !")
        #else:
            ##print('la table EXAMS existe déjà dans la base!!!')
    #___________________
    def createExamsPlayerTable(self):
        sql ='''CREATE TABLE EXAMSPLAYER(
        ply_id INTEGER,
        ex_id INTEGER,
        points INTEGER,
        DATES DATE,
        CONSTRAINT `ply_id` FOREIGN KEY (`ply_id`) REFERENCES `player` (`id`) ON DELETE CASCADE,
        CONSTRAINT `ex_id` FOREIGN KEY (`ex_id`) REFERENCES `exams` (`id`) ON DELETE CASCADE,
        PRIMARY KEY(`ply_id`, `ex_id`)
        
        )'''
        if ('EXAMSPLAYER',) not in self.list_tables():
            self.mycursor.execute(sql)
            ##print(" EXAMSPLAYER elo is created !")
        #else:
            ##print('la table EXAMSPLAYER existe déjà dans la base!!!')
    #___________________
    def createTournamentTable(self):
        sql ='''CREATE TABLE TOURNAMENT(
            id INTEGER AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(80),
            classification VARCHAR(30),
            cadence VARCHAR(20),
            day DATE
            
        )'''
        if ('TOURNAMENT',) not in self.list_tables():
            self.mycursor.execute(sql)
            ##print(" TOURNAMENT elo is created !")
        #else:
            ##print('la table TOURNAMENT existe déjà dans la base!!!')
    #___________________
    def createJoueurTournoiTable(self):
        sql ='''CREATE TABLE JOUEURTOURNOI(
        pl_id INTEGER,
        tr_id INTEGER,
        ranked INTEGER,
        points INTEGER,
        CONSTRAINT `play_id` FOREIGN KEY (`pl_id`) REFERENCES `player` (`id`) ON DELETE CASCADE,
        CONSTRAINT `tr_id` FOREIGN KEY (`tr_id`) REFERENCES `tournament` (`id`) ON DELETE CASCADE,
        PRIMARY KEY(`pl_id`, `tr_id`)
        )'''
        if ('JOUEURTOURNOI',) not in self.list_tables():
            self.mycursor.execute(sql)
            ##print(" JOUEURTOURNOI elo is created !")
        #else:
            ##print('la table JOUEURTOURNOI existe déjà dans la base!!!')
    #___________________
    def createPresenceTable(self):
        sql ='''CREATE TABLE presence(
            p_id INTEGER,
            sess_id INTEGER,
            DAY DATE,
            present INTEGER,
        CONSTRAINT `p_id` FOREIGN KEY (`p_id`) REFERENCES `player` (`id`) ON DELETE CASCADE,
        CONSTRAINT `sess_id` FOREIGN KEY (`sess_id`) REFERENCES `SESSION` (`id`) ON DELETE CASCADE,
        PRIMARY KEY(`p_id`,`sess_id`,`DAY`)
        )'''
        if ('presence',) not in self.list_tables():
            self.mycursor.execute(sql)
            ##print(" Table presence is created !")
        #else:
            ##print('la table presence existe déjà dans la base!!!')
    #___________________

    #___________________
    def createSessionTable(self):
        sql ='''CREATE TABLE SESSION(
            id INTEGER,
            day VARCHAR(10),
            begin VARCHAR(10),
            classes VARCHAR(10),
            level INTEGER,
            title VARCHAR(50),
        PRIMARY KEY(`id`)
        )''' #,`day`,`begin`,`classes`,`level`)
        if ('SESSION',) not in self.list_tables():
            self.mycursor.execute(sql)
            ##print(" Session table is created !")
        #else:
            ##print('table Session is in base!!!')
    #___________________
    #___________________
    def createSessionPlayerTable(self):
        sql ='''CREATE TABLE SESSIONPLAYER(
            pl_ids INTEGER,
            session_ids INTEGER,
            
        CONSTRAINT `pl_ids` FOREIGN KEY (`pl_ids`) REFERENCES `player` (`id`) ON DELETE CASCADE,
        CONSTRAINT `session_ids` FOREIGN KEY (`session_ids`) REFERENCES `SESSION` (`id`) ON DELETE CASCADE,
        PRIMARY KEY(`pl_ids`,`session_ids`)
        )'''
        if ('SESSIONPLAYER',) not in self.list_tables():
            self.mycursor.execute(sql)
            ##print(" SESSIONPLAYER presence is created !")
        #else:
            ##print('la table SESSIONPLAYER existe déjà dans la base!!!')
    #___________________

    def supprimer(self):
        
        myresult = self.list_tables()
        ##print("Voici la liste des tables :")
        #Pfor x in myresult:
                ##print(x)
        reponse = input("Vous etes certain ! Effacer toutes les tables ?(1:oui, 2 ou autres: non")
        if reponse == '1':
                self.delAllTables(myresult)
        else:
                #print("Toutes les tables sont là")
            pass

    #___________________
    def deleteTable(self, table):
        sql = delTable
        self.mycursor = self.mydb.cursor()
        myresult = self.list_tables()
        if (table,) in myresult:
                sql1 = sql + table
                self.mycursor.execute(sql1)
                self.mydb.commit()
                ##print(table, "is deleted")
        #else:
                #print("I can't delete this table!!!")

    #___________________
    def delAllTables(self):
        self.deleteTable(tJoueurTournoi)
        self.deleteTable(tTournament)
        self.deleteTable(tElo)
        self.deleteTable(tScore)
        self.deleteTable(tExamsPlayer)
        self.deleteTable(tExams)
        self.deleteTable(tScore)
        self.deleteTable(tPlayer)
        self.deleteTable(tSeance)
        self.deleteTable(tSessionPlayer)
        self.deleteTable(Tpresence)
    #___________________
    def selectPlayer(self, id):
            self.mycursor = self.mydb.cursor()
            sql = "SELECT * FROM " + tPlayer + " WHERE id="+str(id)+";"
            self.mycursor.execute(sql)
            result = self.mycursor.fetchone()
            self.mycursor.close()
            return result
    #___________________
    def selectListClub(self):
            self.mycursor = self.mydb.cursor()
            sql = "SELECT DISTINCT clubname FROM " + tPlayer+";"
            self.mycursor.execute(sql)
            result = self.mycursor.fetchall()
            self.mycursor.close()
            ##print("liste des clubs DB:", result)
            return result
    #___________________
    def selectNextId(self,table):
            self.mycursor = self.mydb.cursor()
            sql = "select max(id) from "+table+";"
            self.mycursor.execute(sql)
            result = self.mycursor.fetchone()
            self.mycursor.close()
            ##print("le résultat est : ",result)
            if result== (None,):
                  return 1
            return (result[0]+1)

    def selectPlayerLevelRank(self, l):
        self.mycursor = self.mydb.cursor()
        self.mycursor.execute("select name,level,score,GATEGORIE from PLAYER where level=? order by score desc",(l,))
        result = self.mycursor.fetchall()
        
        self.mycursor.close()
        return result
    #___________________  
    def selectAllPlayer(self):
            self.mycursor = self.mydb.cursor()
            sql = "SELECT * FROM " + tPlayer +" order by name ;"
            self.mycursor.execute(sql)
            result = self.mycursor.fetchall()
            self.mycursor.close()
            return result
 
    #___________________
    def insertPlayer(self,data):
            self.mycursor = self.mydb.cursor()
            ##print(data)
            dataIns=[]
            sql = "INSERT INTO "+ tPlayer + """(id,NAME,sex,fed,clubnumber,
            clubname,birthday,GATEGORIE,nelo,fideno,celo,relo,belo,score,title,k,PICTURE,
            level,phone,mail,card) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""  
            self.mycursor.execute(sql,data)
            self.mydb.commit()
            self.mycursor.close()
            ##print(data,"player is added OK!")
    #___________________
    def deleteAllData(self):
        self.mycursor = self.mydb.cursor()
        sql = "DELETE FROM PLAYER ;"
        self.mycursor.execute(sql)
        self.mycursor = self.mydb.cursor()
        sql = "DELETE FROM ELO ;"
        self.mycursor.execute(sql)
        self.mydb.commit()
        sql = "DELETE FROM EXAMS ;"
        self.mycursor.execute(sql)
        self.mydb.commit()
        sql = "DELETE FROM EXAMSPLAYER ;"
        self.mycursor.execute(sql)
        self.mydb.commit()
        self.mycursor.close()

    #___________________
    def deletePlayer(self, id):
            self.mycursor = self.mydb.cursor()
            sql = "DELETE FROM player WHERE player.id='" + str(id) + "';"
            try:
                  self.mycursor.execute(sql)
                  self.mydb.commit()
                  ##print(self.mycursor.rowcount, "record(s) deleted")
                  
                  ##print("les donnéed du joueur ", str(id),": {} sont supprimés".format(sql))
            except:
                  #print("suppression impossible!!!", str(id),": {} sont supprimés".format(sql))
                pass
            finally:
                  self.mycursor.close()
    #___________________
    def updateplayer(self,data):
            self.mycursor = self.mydb.cursor()
            sql = """
                  UPDATE player SET
                  NAME = ?, sex = ?, fed = ?, clubnumber = ?, clubname = ?, 
                  birthday = ?, GATEGORIE = ?, nelo = ?, fideno = ?, celo = ?,
                  belo = ?, relo = ?, score = ?, title = ?,
                  k = ?, PICTURE = ?, level = ?, phone = ?, mail = ?, card = ?
                  WHERE
                  id = ?
                  """        
            self.mycursor.execute(sql,(data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[12],data[13],data[14],data[15],data[16],data[17],data[18],data[19],data[20],data[0]))     
            #print (data)
            ##print('data updated ok',data[0])
            self.mydb.commit()
            self.mycursor.close()
    
    def updateplayerscore(self,data):
            self.mycursor = self.mydb.cursor()
            sql = """
                  UPDATE player SET
                  score = ?
                  WHERE
                  id = ?
                  """        
            self.mycursor.execute(sql,(data[1],data[0]))     
            #print (data)
            ##print('data updated ok',data[0])
            self.mydb.commit()
            self.mycursor.close()
            
    #___________________
    def updateplayerNoRating(self,data):
            self.mycursor = self.mydb.cursor()
            sql = """
                  UPDATE player SET
                  NAME = ?, sex = ?, fed = ?, clubnumber = ?, clubname = ?, 
                  birthday = ?, GATEGORIE = ?, fideno = ?, title = ?,
                  k = ?, PICTURE = ?
                  WHERE
                  id = ?
                  """ 
            
            self.mycursor.execute(sql,(data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8],data[9],data[10],data[11],data[0]))
            #print (data)
            ##print('data updated ok',data[0])
            self.mydb.commit()
            self.mycursor.close()
    #___________________
    def selectEloplayer(self,id):
            self.mycursor = self.mydb.cursor()
            sql = """SELECT * FROM elo WHERE player_id=? ORDER BY DAY desc"""
            self.mycursor.execute(sql,(id,))
            result = self.mycursor.fetchone()
            self.mycursor.close()
            return result
    #___________________
    def selectHistEloplayer(self,id):
            self.mycursor = self.mydb.cursor()
            sql = """SELECT * FROM elo WHERE player_id=? ORDER BY DAY desc"""
            self.mycursor.execute(sql,(id,))
            result = self.mycursor.fetchall()
            self.mycursor.close()
            ##print("la liste des elo est : ",result)
            return result
    #___________________
    def selectElo(self, id,date):
            self.mycursor = self.mydb.cursor()
            sql = """SELECT * FROM elo WHERE player_id=? AND DAY=?;"""
            ##print(sql,(id,date))

            self.mycursor.execute(sql,(id,date))
            result = self.mycursor.fetchone()
            ##print(result)
            self.mycursor.close()
            return result
    #___________________
    def selectAllElo(self):
            self.mycursor = self.mydb.cursor()
            sql = "SELECT * FROM " + tElo +";"
            self.mycursor.execute(sql)
            result = self.mycursor.fetchall()
            self.mycursor.close()
            return result
 
    #___________________
    def insertElo(self,data):
            self.mycursor = self.mydb.cursor()
            ##print(data)
            
            # for i,elt in enumerate(data):
            #       if i not in [8,10,11,12]:
            #             dataIns.append(elt)
            ###print(dataIns)
            sql = "INSERT INTO "+ tElo + """(player_id,CLASSIC,RAPID,BLITZ,NAT,DAY) 
            VALUES (?, ?, ?, ?, ?, ?)"""  
            try:
                  self.mycursor.execute(sql,data)
                  self.mydb.commit()
                  ##print(data,"elo is added OK!")

            except :
                  #print(Exception.__str__)
                  pass
            self.mycursor.close()
            
    #___________________
    def deleteElo(self, id, day):
            self.mycursor = self.mydb.cursor()
            sql = "DELETE FROM elo WHERE player_id = " + str(id) + "AND DAY = " + day + ";"
            try:
                  self.mycursor.execute(sql)
                  self.mydb.commit()
                  self.mycursor.close()
                  ##print("les donnéed du joueur ", str(id), "et date", day, "sont supprimés")
            except:
                  #print("suppression impossible!!!")
                  pass

    #___________________
    def updateElo(self,data):
            self.mycursor = self.mydb.cursor()
            sql = """
                  UPDATE elo SET
                  CLASSIC = ?, RAPID = ?, BLITZ = ?, NAT = ?
                  WHERE
                  player_id = ? AND DAY = ?
                  """ 
            self.mycursor.execute(sql,(data[1],data[2],data[3],data[4],data[0],data[5]))
            self.mydb.commit()
            self.mycursor.close()

#___________________  


#___________________  
    def selectAllExams(self):
            self.mycursor = self.mydb.cursor()
            sql = "SELECT * FROM " + tExams +";"
            self.mycursor.execute(sql)
            result = self.mycursor.fetchall()
            self.mycursor.close()
            return result
 
    def selectExam(self, id):
        self.mycursor = self.mydb.cursor()
        sql = "SELECT * FROM " + tExams +" WHERE id = {};".format(id)
        self.mycursor.execute(sql)
        result = self.mycursor.fetchone()
        self.mycursor.close()
        return result
    #___________________
    def insertExam(self,data):
            id = self.selectNextId('EXAMS')
            self.mycursor = self.mydb.cursor()
            ##print(data)
            dataIns=[id] + data
            sql = "INSERT INTO "+ tExams + """(id,NAMES,DATES) 
            VALUES (?, ?, ?)"""  
            self.mycursor.execute(sql,dataIns)
            self.mydb.commit()
            self.mycursor.close()
            ##print(dataIns,"Exam is added OK!")
    #___________________
    def deleteAllExams(self):
        self.mycursor = self.mydb.cursor()
        sql = "DELETE FROM EXAMS ;"
        self.mycursor.execute(sql)
        self.mydb.commit()
        self.mycursor.close()

    #___________________
    def deleteExam(self, id):
            self.mycursor = self.mydb.cursor()
            sql = "DELETE FROM EXAMS WHERE EXAMS.id=" + str(id) + ";"
            try:
                  self.mycursor.execute(sql)
                  self.mydb.commit()
                  ##print(self.mycursor.rowcount, "record(s) deleted")
                  
                  ##print("les donnée Exam ", id ,": {} sont supprimés".format(sql))
            except:
                  #print("suppression impossible!!!", id,": {} sont supprimés".format(sql))
                  pass

            finally:
                  self.mycursor.close()
    #___________________
    def updateExam(self,data):
            self.mycursor = self.mydb.cursor()
            sql = """
                  UPDATE EXAMS SET
                  NAMES = ?, DATES = ?
                  WHERE
                  id = ?
                  """        
            self.mycursor.execute(sql,(data[1],data[2],data[0]))     
            #print (data)
            ##print('data updated ok',data[0])
            self.mydb.commit()
            self.mycursor.close()
#___________________                                    ___________________  
#                               ____ EXAMSPLAYER ____
#___________________                                    ___________________  
    def selectAllExamsPlayer(self):
            self.mycursor = self.mydb.cursor()
            sql = "SELECT * FROM " + tExamsPlayer +";"
            self.mycursor.execute(sql)
            result = self.mycursor.fetchall()
            self.mycursor.close()
            return result
    
    def selectExamsPlayer(self, idpl, idex):
        self.mycursor = self.mydb.cursor()
        sql = "SELECT * FROM " + tExamsPlayer +" WHERE ply_id=" + str(idpl) + " AND ex_id=" + str(idex) +";"
        ##print(sql)
        self.mycursor.execute(sql)
        result = self.mycursor.fetchall()
        self.mycursor.close()
        ##print("exam/player :",result)
        return result

    def selectExamsPlayerDate(self, idpl, date):
        self.mycursor = self.mydb.cursor()
        sql = "SELECT * FROM " + tExamsPlayer +" WHERE ply_id={} AND DATES='{}';".format(idpl,date)
        ##print(sql)
        self.mycursor.execute(sql)
        result = self.mycursor.fetchall()
        self.mycursor.close()
        ##print("exam/player :",result)
        return result


    def selectCountExHW(self, name):
        self.mycursor = self.mydb.cursor()
        sql = "SELECT COUNT(*) FROM EXAMS WHERE NAMES LIKE '{}%'".format(name)
        ##print(sql)
        self.mycursor.execute(sql)
        result = self.mycursor.fetchone()
        return(result[0]+1)
        

    def selectExamCross(self, exId, score):
        self.mycursor = self.mydb.cursor()
        sql = "SELECT PLAYER.NAME,EXAMSPLAYER.points,EXAMSPLAYER.DATES FROM PLAYER INNER JOIN EXAMSPLAYER ON PLAYER.id=EXAMSPLAYER.ply_id WHERE "
        if score == -8888:
            sql+="EXAMSPLAYER.points=-8888 AND EXAMSPLAYER.ex_id={} ".format(exId)
        else:
            sql+="EXAMSPLAYER.points>{} AND EXAMSPLAYER.ex_id={}".format(score,exId)
        sql+=" ORDER BY EXAMSPLAYER.points DESC"
        ##print("Requte : ",sql)
        self.mycursor.execute(sql)
        result = self.mycursor.fetchall()
        self.mycursor.close()
        ##print("exam/player :",result)
        return result
    #___________________
    def insertExamPlayer(self,data):
            #id = self.selectNextId(tExamsPlayer)
            self.mycursor = self.mydb.cursor()
            ##print(data)
            #dataIns=[id] + data
            sql = "INSERT INTO "+ tExamsPlayer + """(ply_id,ex_id,points,DATES) 
            VALUES (?, ?, ?, ?)"""  
            self.mycursor.execute(sql,data)
            self.mydb.commit()
            self.mycursor.close()
            ##print(data,"Exam is added OK!")
    #___________________
    def deleteAllExamsPlayer(self):
        self.mycursor = self.mydb.cursor()
        sql = "DELETE FROM EXAMSPLAYER ;"
        self.mycursor.execute(sql)
        self.mydb.commit()
        self.mycursor.close()

    #___________________
    def deleteExamPlayer(self, idpl,idex):
            self.mycursor = self.mydb.cursor()
            sql = "DELETE FROM EXAMSPLAYER WHERE EXAMSPLAYER.ply_id=" + str(idpl) + " AND EXAMSPLAYER.ex_id=" + str(idex) + ";"
            try:
                self.mycursor.execute(sql)
                self.mydb.commit()
                  ##print(self.mycursor.rowcount, "record(s) deleted")
                  
                  ##print("les donnée Exam ", idpl ,": {} sont supprimés".format(sql))
            except:
                  #print("suppression impossible!!!", idpl,": {} sont supprimés".format(sql))
                pass
            finally:
                self.mycursor.close()
    #___________________
    def updateExamPlayer(self,data):
            self.mycursor = self.mydb.cursor()
            sql = """
                  UPDATE EXAMSPLAYER SET
                  points = ?, DATES = ?
                  WHERE
                  ply_id = ? AND ex_id = ?
                  """        
            self.mycursor.execute(sql,(data[2],data[3],data[0],data[1]))     
            #print (data)
            ##print('data updated ok',data[0])
            self.mydb.commit()
            self.mycursor.close()

    
#___________________                                    ___________________  
#                               ____ Session Table  ____
#___________________                                    ___________________  
    def selectAllSession(self):
            self.mycursor = self.mydb.cursor()
            sql = "SELECT * FROM " + tSeance +";"
            self.mycursor.execute(sql)
            result = self.mycursor.fetchall()
            self.mycursor.close()
            return result
    
    def selectSession(self, day):
        self.mycursor = self.mydb.cursor()
        sql = "SELECT * FROM " + tSeance +" WHERE day='" + day +"';"
        ##print(sql)
        self.mycursor.execute(sql)
        result = self.mycursor.fetchall()
        self.mycursor.close()
        ##print("Session for {}:".format(day),result)
        return result
 
    def selectSessionT(self, title):
        self.mycursor = self.mydb.cursor()
        sql = "SELECT * FROM " + tSeance +" WHERE title='" + title +"';"
        ##print(sql)
        self.mycursor.execute(sql)
        result = self.mycursor.fetchall()
        self.mycursor.close()
        ##print("Session for {}:".format(title),result)
        return result

    def selectSessionl(self, l):
        self.mycursor = self.mydb.cursor()
        sql = "SELECT * FROM " + tSeance +" WHERE level=" + str(l) +";"
        ##print(sql)
        self.mycursor.execute(sql)
        result = self.mycursor.fetchall()
        self.mycursor.close()
        ##print("Session for {}:".format(title),result)
        return result

   
    #___________________
    def insertSession(self,data):
            #id = self.selectNextId(tExamsPlayer)
            self.mycursor = self.mydb.cursor()
            ##print(data)
            #dataIns=[id] + data
            sql = "INSERT INTO "+ tSeance + """(id,day,begin,classes,level,title) 
            VALUES (?, ?, ?, ?, ?, ?)"""  
            self.mycursor.execute(sql,data)
            self.mydb.commit()
            self.mycursor.close()
            ##print(data,"Session is added OK!")
    #___________________
    def deleteAllSession(self):
        self.mycursor = self.mydb.cursor()
        sql = "DELETE FROM SESSION ;"
        self.mycursor.execute(sql)
        self.mydb.commit()
        self.mycursor.close()

    #___________________
    def deleteSession(self, title):
            self.mycursor = self.mydb.cursor()
            sql = "DELETE FROM SESSION WHERE SESSION.title={};".format(title)
            try:
                  self.mycursor.execute(sql)
                  self.mydb.commit()
                  ##print(self.mycursor.rowcount, "record(s) deleted")
                  
                  ##print("les donnée Exam ", title ,": {} sont supprimés".format(sql))
            except:
                  #print("suppression impossible!!!", title,": {} sont supprimés".format(sql))
                pass
            finally:
                  self.mycursor.close()
    #___________________
    def updateSession(self,data):
            self.mycursor = self.mydb.cursor()
            sql = """
                  UPDATE SESSION SET
                  day = ?, begin = ?, classes = ?, level = ?, title = ?
                  WHERE
                  title = ?
                  """        
            self.mycursor.execute(sql,(data[1],data[2],data[3],data[4],data[5],data[0]))     
            #print (data)
            ##print('data updated ok',data[0])
            self.mydb.commit()
            self.mycursor.close()

#___________________                                    ___________________  
#                               ____ SESSIONPLAYER Table  ____
#___________________                                    ___________________  
    def selectAllSessionPl(self):
            self.mycursor = self.mydb.cursor()
            sql = "SELECT * FROM " + tSessionPlayer +";"
            self.mycursor.execute(sql)
            result = self.mycursor.fetchall()
            self.mycursor.close()
            return result

    def selectSessionPl(self,data):
            self.mycursor = self.mydb.cursor()
            sql = "SELECT * FROM " + tSessionPlayer +" WHERE pl_ids='"+str(data[0])+"' AND session_ids='"+str(data[1])+"';" 
            self.mycursor.execute(sql)
            result = self.mycursor.fetchone()
            ##print("le resultat est:", result)
            self.mycursor.close()
            return result
    
    def selectSessionFromPlayter(self, id):
        self.mycursor = self.mydb.cursor()
        sql = "SELECT SESSION.id,SESSION.title FROM " + tSeance +" INNER JOIN SESSIONPLAYER ON SESSION.id=SESSIONPLAYER.session_ids WHERE "
        sql+="SESSIONPLAYER.pl_ids={} ".format(id)
        ##print(sql)
        self.mycursor.execute(sql)
        result = self.mycursor.fetchall()
        self.mycursor.close()
        ##print("Session for {}:".format(id),result)
        return result
    
   
   
    #___________________
    def insertSessionPlayer(self,data):
            #id = self.selectNextId(tExamsPlayer)
            self.mycursor = self.mydb.cursor()
            ##print(data)
            #dataIns=[id] + data
            sql = "INSERT INTO "+ tSessionPlayer + """(pl_ids,session_ids) 
            VALUES (?, ?)"""  
            self.mycursor.execute(sql,data)
            self.mydb.commit()
            self.mycursor.close()
            ##print(data,"SessionPlayer is added OK!")
    #___________________
    def deleteAllSessionPlayer(self):
        self.mycursor = self.mydb.cursor()
        sql = "DELETE FROM SESSIONPLAYER ;"
        self.mycursor.execute(sql)
        self.mydb.commit()
        self.mycursor.close()

    #___________________
    def deleteSessionPlayer(self, data):
            self.mycursor = self.mydb.cursor()
            sql = "DELETE FROM SESSIONPLAYER WHERE SESSIONPLAYER.pl_ids=" + str(data[0]) + " AND SESSIONPLAYER.session_ids="+str(data[1])+";"
            try:
                  self.mycursor.execute(sql)
                  self.mydb.commit()
                  ##print(self.mycursor.rowcount, "record(s) deleted")
                  
                  ##print("les donnée SessionPlayer ", data ,": {} sont supprimés".format(sql))
            except:
                  #print("suppression impossible!!!", data,": {} sont supprimés".format(sql))
                  return -1

            finally:
                  self.mycursor.close()
    #___________________
#___________________                                    ___________________  
#                               ____ presence Table  ____
#___________________                                    ___________________  
#p_id INTEGER, sess_id INTEGER, DAY DATE, present INTEGER,
    def insertPresence(self,data):
            #id = self.selectNextId(tExamsPlayer)
            self.mycursor = self.mydb.cursor()
            ##print("presence added ok: ",data)
            #dataIns=[id] + data
            sql = "INSERT INTO "+ Tpresence + """(p_id,sess_id,DAY,present) 
            VALUES (?, ?, ?, ?)"""  
            self.mycursor.execute(sql,data)
            self.mydb.commit()
            self.mycursor.close()
            ##print(data,"SessionPlayer is added OK!")
    def selectAllPresence(self):
        self.mycursor = self.mydb.cursor()
        sql = "select * from presence"
        self.mycursor.execute(sql)
        result = self.mycursor.fetchall()
        #print("toutes les presences : ",result)
        self.mydb.commit()
        self.mycursor.close()
    def selectPresence(self,data):
            self.mycursor = self.mydb.cursor()
            sql = "SELECT * FROM  presence WHERE p_id = ? AND sess_id = ? AND DAY = ? ;" 
            self.mycursor.execute(sql,data)
            result = self.mycursor.fetchone()
            ##print("le resultat est:", result)
            self.mycursor.close()
            return result
    
    def selectPresenceStatus(self,pid,level,type):
        self.mycursor = self.mydb.cursor()
        sql = "SELECT COUNT(*) FROM " + Tpresence +" INNER JOIN Session ON presence.sess_id=Session.id WHERE "
        sql+="presence.p_id={} AND Session.level={} and presence.present={} ".format(pid, level,type)
        #print(sql)
        self.mycursor.execute(sql)
        result = self.mycursor.fetchone()
        #print("le resultat pour presence de type ",type," est:", result)
        self.mycursor.close()
        return result[0]

    def selectPresenceFromPlayter(self, data):
        self.mycursor = self.mydb.cursor()
        sql = "SELECT SESSION.title,SESSION.begin,presence.DAY,presence.present  FROM " + tSeance +" INNER JOIN presence ON SESSION.id=presence.sess_id WHERE "
        sql+="presence.p_id={} AND presence.DAY BETWEEN '{}' and '{}' ".format(data[0], data[1], data[2])
        ##print(sql)
        self.mycursor.execute(sql)
        result = self.mycursor.fetchall()
        self.mycursor.close()
        ##print("Session for {}:".format(data),result)
        return result


    def selectPlayerFromSeance(self, data):
        self.mycursor = self.mydb.cursor()
        sql = "SELECT PLAYER.name  FROM " + tPlayer +" INNER JOIN SESSIONPLAYER ON PLAYER.id=SESSIONPLAYER.pl_ids WHERE "
        sql+="SESSIONPLAYER.session_ids={}".format(data)
        ##print(sql)
        self.mycursor.execute(sql)
        result = self.mycursor.fetchall()
        self.mycursor.close()
        ##print("Session for {}:".format(data),result)
        return result

    def updatePresence(self,data):
            self.mycursor = self.mydb.cursor()
            sql = """
                  UPDATE presence SET
                  present = ?
                  WHERE
                  p_id = ? AND sess_id = ? AND DAY = ?
                  """        
            self.mycursor.execute(sql,(data[3],data[0],data[1],data[2]))     
            #print (data)
            ##print('data updated ok',data[0])
            self.mydb.commit()
            self.mycursor.close()

    def deletePresence(self, data):
            self.mycursor = self.mydb.cursor()
            sql = "DELETE FROM presence WHERE presence.p_id = ? AND presence.sess_id = ? AND presence.DAY = ?" 
            try:
                  self.mycursor.execute(sql, data)
                  self.mydb.commit()
                  ##print(self.mycursor.rowcount, "record(s) deleted")
                  
                  ##print("les donnée presence ", data ,": {} sont supprimés".format(sql))
            except:
                  #print("suppression impossible!!!", data,": {} sont supprimés".format(sql))
                pass
            finally:
                  self.mycursor.close()

#___________________                                    ___________________  
#                               ____ TOURNAMENT Table  ____
#___________________                                    ___________________  
    def insertEvent(self,data):
        #id = self.selectNextId(tExamsPlayer)
        self.mycursor = self.mydb.cursor()
        ##print("Event added ok: ",data)
        #dataIns=[id] + data
        sql = "INSERT INTO "+ tTournament + """(id,title,classification,cadence,day) 
        VALUES (?, ?, ?, ?, ?)"""  
        self.mycursor.execute(sql,data)
        self.mydb.commit()
        self.mycursor.close()
        ##print(data,"Event is added OK!")

    def updateEvent(self,data):
            self.mycursor = self.mydb.cursor()
            sql = """
                  UPDATE TOURNAMENT SET
                  title = ?, classification = ?, cadence = ?, day = ?
                  WHERE
                  id = ? 
                  """        
            self.mycursor.execute(sql,(data[1],data[2],data[3],data[4],data[0]))     
            #print (data)
            ##print('data updated ok',data[0])
            self.mydb.commit()
            self.mycursor.close()

    def selectAllEvents(self):
            self.mycursor = self.mydb.cursor()
            sql = "SELECT * FROM " + tTournament +";"
            self.mycursor.execute(sql)
            result = self.mycursor.fetchall()
            self.mycursor.close()
            return result

    def deleteEvent(self, id):
            self.mycursor = self.mydb.cursor()
            sql = "DELETE FROM TOURNAMENT WHERE id = {}".format(id) 
            try:
                  self.mycursor.execute(sql)
                  self.mydb.commit()
                  ##print(self.mycursor.rowcount, "record(s) deleted")
                  
                  ##print("les donnée event ", id ,": {} sont supprimés".format(sql))
            except:
                  #print("suppression impossible!!!", id,": {} sont supprimés".format(sql))
                pass
            finally:
                  self.mycursor.close()
    
    def selectEvent(self,name):
            self.mycursor = self.mydb.cursor()
            sql = "SELECT * FROM  TOURNAMENT WHERE title LIKE '{}';".format(name) 
            self.mycursor.execute(sql)
            result = self.mycursor.fetchone()
            ##print("le resultat est:", result)
            self.mycursor.close()
            return result
#___________________                                    ___________________  
#                               ____ JOUEURTOURNOI Table  ____
#___________________                                    ___________________  
# id, title, classification, cadence, day
# JOUEURTOURNOI, pl_id, tr_id, ranked, points,           
    def insertEventPLayer(self,data):
        #id = self.selectNextId(tExamsPlayer)
        self.mycursor = self.mydb.cursor()
        ##print("Event to player added ok: ",data)
        #dataIns=[id] + data
        sql = "INSERT INTO "+ tJoueurTournoi + """(pl_id,tr_id,ranked,points) 
        VALUES (?, ?, ?, ?)"""  
        self.mycursor.execute(sql,data)
        self.mydb.commit()
        self.mycursor.close()
        ##print(data,"Event to player is added OK!")    

    def selectEventPlayer(self,idpl,idev):
            self.mycursor = self.mydb.cursor()
            sql = "SELECT * FROM  JOUEURTOURNOI WHERE pl_id = {} and tr_id = {};".format(idpl, idev) 
            self.mycursor.execute(sql)
            result = self.mycursor.fetchone()
            ##print("le resultat est:", result)
            self.mycursor.close()
            return result        

    def updateEventPlayer(self,data):
            self.mycursor = self.mydb.cursor()
            sql = """
                  UPDATE JOUEURTOURNOI SET
                  ranked = ?, points = ?
                  WHERE
                  pl_id = ? AND tr_id = ?
                  """        
            self.mycursor.execute(sql,(data[2],data[3],data[0],data[1]))     
            #print (data)
            ##print('data updated ok',data[0])
            self.mydb.commit()
            self.mycursor.close() 

    def selectEventsPlayer(self, data):
        self.mycursor = self.mydb.cursor()
        sql = "SELECT TOURNAMENT.title, TOURNAMENT.classification, TOURNAMENT.cadence, TOURNAMENT.day, JOUEURTOURNOI.ranked, JOUEURTOURNOI.points   FROM " + tTournament +" INNER JOIN JOUEURTOURNOI ON JOUEURTOURNOI.tr_id=TOURNAMENT.id WHERE "
        sql+="JOUEURTOURNOI.pl_id={} AND TOURNAMENT.DAY BETWEEN '{}' AND '{}' ".format(data[0], data[1], data[2])
        ##print(sql)
        self.mycursor.execute(sql)
        result = self.mycursor.fetchall()
        self.mycursor.close()
        ##print("Events for {}:".format(data),result)
        return result

#___________________                                    ___________________  
#                               ____ score Table  ____
#___________________                                    ___________________  
    def insertScorePLayer(self,data):
        #id = self.selectNextId(tExamsPlayer)
        self.mycursor = self.mydb.cursor()
        ##print("Score to player added ok: ",data)
        #dataIns=[id] + data
        sql = "INSERT INTO "+ tScore + """(p_ids,DAY,levels,score,raison) 
        VALUES (?, ?, ?, ?, ?)"""  
        try:
            self.mycursor.execute(sql,data)
            self.mydb.commit()
            #print(data,"Score to player is added OK!")
        except:
            #print("Ajout de score est impossible ")
            pass
        finally:
            self.mycursor.close()
            
    def selectAllScore(self):
            self.mycursor = self.mydb.cursor()
            sql = "SELECT * FROM  score;" 
            self.mycursor.execute(sql)
            result = self.mycursor.fetchall()
            #print("Tous les scores :", result)
            self.mycursor.close()
            return result

    def selectScore(self,id,date,r):
            self.mycursor = self.mydb.cursor()
            sql = "SELECT * FROM  score WHERE p_ids={} and DAY='{}' and raison={};".format(id,date,r) 
            self.mycursor.execute(sql)
            result = self.mycursor.fetchone()
            #print("le resultat est:", result)
            self.mycursor.close()
            return result

    def selectScoreType(self,id,r,l):
            self.mycursor = self.mydb.cursor()
            sql = "SELECT * FROM  score WHERE p_ids={} and raison={} and levels={} ORDER BY DAY;".format(id,r,l) 
            self.mycursor.execute(sql)
            result = self.mycursor.fetchall()
            #print("le resultat est:", result)
            self.mycursor.close()
            return result
    
    def updateScorePlayer(self,id,val,d,r):
            self.mycursor = self.mydb.cursor()
            
            sql = """
                  UPDATE score SET
                  score = ?
                  WHERE
                  p_ids = ? AND DAY = ? AND raison = ?
                  """   
            try:    
                self.mycursor.execute(sql,(val,id,d,r))     
                self.mydb.commit()
                #print('data updated ok',(val,d,r))
            except:
                #print("Update de score est impossible ")
                pass
            finally:
                self.mycursor.close() 

    #___________________
    def deletedata(self, table):
            self.mycursor = self.mydb.cursor()
            sql = "DELETE FROM {} ;".format(table)
            try:
                  self.mycursor.execute(sql)
                  self.mydb.commit()   
            except:
                pass
            finally:
                  self.mycursor.close()
#  p_ids DAY levels presence exam homework events raison

#___________________                                    ___________________  
#                               ____ payment Table  ____
#___________________                                    ___________________  
    def insertPayment(self,data):
        res = self.selectPaymentTable(data[0],data[2],data[4])
        r = 1
        self.mycursor = self.mydb.cursor()
        if res == None:
            sql = "INSERT INTO "+ Tpayment + """(j_id,amount,month,day,year) 
        VALUES (?, ?, ?, ?, ?)"""  

        else:
            data = (data[1],data[3],data[0],data[2],data[4])
            sql = """
                  UPDATE payment SET
                  amount = ?,day = ?
                  WHERE
                  j_id = ? AND month = ? AND year = ?
                  """   
            r = 0
        try:
            self.mycursor.execute(sql,data)
            self.mydb.commit()
        except:
            pass
        finally:
            self.mycursor.close()
        return r

    def insertVip(self,data):
        res =  self.selectVipTable(data[0])
        self.mycursor = self.mydb.cursor()
        r = 1
        if res == None:
            sql = "INSERT INTO "+ Tvip + """(jo_id,amount,month,year,number) VALUES (?, ?, ?, ?, ?)"""  
        else:
            data = (data[1],data[2],data[3],data[4], data[0])
            sql = """
                  UPDATE vip SET
                  amount = ?, month = ?, year = ?, number = ?
                  WHERE
                  jo_id = ? 
                  """   
            r = 0
        try:
            self.mycursor.execute(sql,data)
            self.mydb.commit()
        except:
            pass
        finally:
            self.mycursor.close()
        return r
    def selectPaymentTable(self,id,m,a):
            self.mycursor = self.mydb.cursor()
            sql = "SELECT pl.name, py.amount FROM  payment as py inner join PLAYER as pl on pl.id = py.j_id WHERE py.j_id={} and py.month={} and py.year={} ORDER BY pl.name;".format(id,m,a) 
            self.mycursor.execute(sql)
            result = self.mycursor.fetchone()
            #print("le resultat est:", result)
            self.mycursor.close()
            return result
    
    def selectPaymentView(self,m,a):
            self.mycursor = self.mydb.cursor()
            sql = "SELECT pl.name, py.amount, py.day FROM  payment as py inner join PLAYER as pl on pl.id = py.j_id WHERE py.month={} and py.year={} ORDER BY pl.name;".format(m,a) 
            self.mycursor.execute(sql)
            result = self.mycursor.fetchall()
           # print("le resultat est:", result)
            self.mycursor.close()
            return result
    
    def deletePayment(self, id,m,a):
        res = self.selectPaymentTable(id,m,a)
        if res != None:
            self.mycursor = self.mydb.cursor()
            sql = "DELETE FROM payment WHERE j_id = {} and month = {} and year = {}".format(id,m,a)
            try:
                self.mycursor.execute(sql)
                self.mydb.commit()   
            except:
                pass
            finally:
                self.mycursor.close()
            return 1
        return 0
        
    
    def selectVipTable(self,id):
            self.mycursor = self.mydb.cursor()
            sql = "SELECT pl.name, py.amount FROM  vip as py inner join PLAYER as pl on pl.id = py.jo_id WHERE py.jo_id={} ORDER BY pl.name;".format(id) 
            self.mycursor.execute(sql)
            result = self.mycursor.fetchone()
            #print("le resultat est:", result)
            self.mycursor.close()
            return result

    def selectVipView(self):
            self.mycursor = self.mydb.cursor()
            sql = "SELECT pl.name, py.amount, py.month, py.year, py.number FROM  vip as py inner join PLAYER as pl on pl.id = py.jo_id ORDER BY pl.name;"
            self.mycursor.execute(sql)
            result = self.mycursor.fetchall()
            #print("le resultat est:", result)
            self.mycursor.close()
            return result
# j_id , amount , month , year , number
#.......................        
def main(args):
    mabase = Mabase(base)

#.......................
if __name__=="__main__":
    main(sys.argv)