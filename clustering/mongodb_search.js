// http://docs.mongodb.org/manual/reference/operator/query/text/
// 
db.result.createIndex({
                             title: "text",
                             description: "text",
                             address: "text"
                           })

db.result.find( { $text: { $search: "\"antiguo de la ciudad\"" } } ) // NO UTF-8 SUPPORT WTF???!
db.result.find({title:{$regex:/hotel/,$options:"$i"}})
db.result.find({description:{$regex: "escapada romántic",$options:"$i"}})
db.result.dropIndexes()