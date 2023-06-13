/* global use, db */
// MongoDB Playground
// To disable this template go to Settings | MongoDB | Use Default Template For Playground.
// Make sure you are connected to enable completions and to be able to run a playground.
// Use Ctrl+Space inside a snippet or a string literal to trigger completions.
// The result of the last command run in a playground is shown on the results panel.
// By default the first 20 documents will be returned with a cursor.
// Use 'console.log()' to print to the debug output.
// For more documentation on playgrounds please refer to
// https://www.mongodb.com/docs/mongodb-vscode/playgrounds/

// Select the database to use.
use('challenge');

// Insert a few documents into the sales collection.


// Here we run an aggregation and open a cursor to the results.
// Use '.toArray()' to exhaust the cursor to return the whole result set.
// You can use '.hasNext()/.next()' to iterate through the cursor page by page.
db.getCollection('transactions').aggregate([
    // Find all of the sales that occurred in 2014.
    { $match: { $or: [{ signature: { $ne: null } }, { signature: { $exists: true } }] } },
]);

// db.getCollection('transactions').updateMany(
//     // Find all of the sales that occurred in 2014.
//     { signature: { $or: [{ $ne: null }, { $exists: false }] } },
//     [{ $unset: ['signature'] }],
// );

// db.getCollection('keys').aggregate([
//     // Find all of the sales that occurred in 2014.
//     {$match: {
//         _id:ObjectId('647ea10dbca375a56ab52d7a')
//     }},
// ]);

// db.getCollection('keys').updateMany(
//     // Find all of the sales that occurred in 2014.
//     { last_used: { $ne: null } },
//     [{ $unset: ['last_used'] }],
// );


db.getCollection('keys').findOne({
    '$or': [
        { 'locked': false },
        { 'expire': { '$lt': Date() } },
    ]
},
    // Find all of the sales that occurred in 2014.
    { last_used: { $ne: null } },
    [{ $unset: ['last_used'] }],
);


// db.getCollection('keys').aggregate([
//     // Find all of the sales that occurred in 2014.
//     { $match: { last_used: { $eq: null } } },
//     {$sort: {
//       _id: -1
//     }}
// ]);
