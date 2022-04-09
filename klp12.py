import time
from datetime import datetime
import mysql.connector #digunakan untuk mengimport library mysql
i = 1

while(i):
    mydb_local = mysql.connector.connect( #data-data pada variabel ini dikoneksikan menggunakan sintaks mysql.connector.connect()
    host="sql6.freemysqlhosting.net", #merupakan nama host yang digunakan
    user="sql6484575", #merupakan nama user yang digunakan
    passwd="wFb38tlJyG", #diisi apabila terdapat password didalamnya
    database="sql6484575", #merupakan nama database yang digunakan
    )

    mydb_host = mysql.connector.connect(
        host="db4free.net",
        user="ardhiya",
        passwd="kK3SVnb8DMWSS@-",
        database="db_modul1",
    )

    mycursor = mydb_local.cursor() #digunakan untuk pengolahan data CRUD yang diambil dari database
    mycursor_host = mydb_host.cursor() #digunakan untuk pengolahan data CRUD yang diambil dari database


    print("====================== SYNC LOCAL ======================")
    sync = []
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    mycursor.execute("SELECT * FROM tb_sync WHERE id >=(SELECT MAX(id)-2 FROM tb_sync) AND id <=(SELECT MAX(id) FROM tb_sync);")
    for i in mycursor.fetchall():
        idx = i[0]
        id_tabel = i[1]
        aksi = i[2]
        sinkronisasi = i[3]
        sync.append(i)
        # print(sync)

        for i in range(0,3):
            print('.')
            time.sleep(1)

        if str(sinkronisasi) == "None":
                
            if aksi == "insert":
                mycursor.execute("select * from tb_transaksi where id ="+str(id_tabel)+"")
                for i in mycursor.fetchall():
                    pegawai = i[1]
                    customer = i[2]
                    barang = i[3]
                    harga = i[4]

                    sql = "insert into tb_transaksi(pegawai, customer, barang, harga, tgl_transaksi, updated_at, status_transaksi) values (%s, %s, %s, %s, %s, %s, %s)"
                    val = (pegawai, customer, barang, harga, timestamp, None, "pending")

                    mycursor_host.execute(sql, val)
                    mydb_host.commit()
                    print("Berhasil menambah transaksi tabel " +str(id_tabel)+ " pada db host")

                    sinkron = "update tb_sync set sinkronisasi ='telah sinkron' where id="+str(idx)+""
                    mycursor.execute(sinkron)
                    mydb_local.commit()
            

            elif aksi == "update":
                mycursor.execute("select * from tb_transaksi where id ="+str(id_tabel)+"")
                for i in mycursor.fetchall():
                    status = i[5]

                    sql = "update tb_transaksi set updated_at ='"+timestamp+"', status_transaksi ='"+status+"' where id="+str(id_tabel)+" "
                    mycursor_host.execute(sql)
                    mydb_host.commit()
                    print("Berhasil mengupdate transaksi tabel " +str(id_tabel)+ " pada db host")

                    sinkron = "update tb_sync set sinkronisasi ='telah sinkron' where id="+str(idx)+""
                    mycursor.execute(sinkron)
                    mydb_local.commit()


            elif aksi == "delete":
                sql = "delete from tb_transaksi where id="+str(id_tabel)+" "
                mycursor_host.execute(sql)
                mydb_host.commit()
                print("Berhasil menghapus transaksi tabel " +str(id_tabel)+ " pada db host")

                sinkron = "update tb_sync set sinkronisasi ='telah sinkron' where id="+str(idx)+""
                mycursor.execute(sinkron)
                mydb_local.commit()

            else:
                print("Kesalahan histori sinkronisasi")


        else:
            print("Data " +str(idx)+ " telah tersinkronisasi")


    print("====================== SYNC HOST ======================")
    sync = []
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')    

    mycursor_host.execute("SELECT * FROM tb_sync WHERE id >=(SELECT MAX(id)-2 FROM tb_sync) AND id <=(SELECT MAX(id) FROM tb_sync)")
    for i in mycursor_host.fetchall():
        idx = i[0]
        id_tabel = i[1]
        aksi = i[2]
        sinkronisasi = i[3]
        sync.append(i)
        # print(sync)

        for i in range(0,3):
            print('.')
            time.sleep(1)

        if str(sinkronisasi) == "None":
                
            
            if aksi == "update":
                mycursor_host.execute("select * from tb_transaksi where id ="+str(id_tabel)+"")
                for i in mycursor_host.fetchall():
                    status = i[5]

                    sql = "update tb_transaksi set updated_at ='"+timestamp+"', status_transaksi ='"+status+"' where id="+str(id_tabel)+" "
                    mycursor.execute(sql)
                    mydb_local.commit()
                    print("Berhasil mengupdate transaksi tabel " +str(id_tabel)+ " pada db local")

                    sinkron = "update tb_sync set sinkronisasi ='telah sinkron' where id="+str(idx)+""
                    mycursor_host.execute(sinkron)
                    mydb_host.commit()

                    mycursor.execute("DELETE FROM tb_sync WHERE id_tabel IS NULL")
                    mydb_local.commit()

            else:
                print("Kesalahan histori sinkronisasi")


        else:
            print("Data " +str(idx)+ " telah tersinkronisasi")


    print("====================== READ ======================")
    print("Data Local")
    mycursor.execute("select * from tb_transaksi") #digunakan untuk mengeksekusi sintaks sql yang dituliskan
    for i in mycursor.fetchall(): #mengambil masing-masing data dengan menggunakan fetch sehingga data tampil per row/baris
        idx = i[0] #karena data yang ditampilkan berupa tupel maka diambil per indeks array untuk mendapatkan data mentah
        pegawai = i[1]
        customer = i[2]
        barang = i[3]
        harga = i[4]
        status_transaksi = i[5]
        tgl_transaksi = i[6]
        updated_at = i[7]
        deleted_at = i[8]
        print(str(idx)+" "+pegawai+" "+customer+" "+barang+" "+str(harga)+" "+str(status_transaksi)+" "+str(tgl_transaksi)+" "+str(updated_at)+" "+str(deleted_at))
        #data mentah (value) kemudian di print sehingga tampil

    print("====================== READ ======================")
    print("Data Host")
    mycursor_host.execute("select * from tb_transaksi") #digunakan untuk mengeksekusi sintaks sql yang dituliskan
    for i in mycursor_host.fetchall(): #mengambil masing-masing data dengan menggunakan fetch sehingga data tampil per row/baris
        idx = i[0] #karena data yang ditampilkan berupa tupel maka diambil per indeks array untuk mendapatkan data mentah
        pegawai = i[1]
        customer = i[2]
        barang = i[3]
        harga = i[4]
        status_transaksi = i[5]
        tgl_transaksi = i[6]
        updated_at = i[7]
        deleted_at = i[8]
        print(str(idx)+" "+pegawai+" "+customer+" "+barang+" "+str(harga)+" "+str(status_transaksi)+" "+str(tgl_transaksi)+" "+str(updated_at)+" "+str(deleted_at))
        #data mentah (value) kemudian di print sehingga tampil

    i=0
