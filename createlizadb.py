
import dbm



elizadb = dbm.open('elizadatabase', 'c')
elizadb['15169467918']  = "undefined"
print ( elizadb['15169467918'])
elizadb.close
