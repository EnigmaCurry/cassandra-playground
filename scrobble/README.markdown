This is a demo app for me to learn and start playing around with
Cassandra. One of the biggest advantages of Cassandra is it's
availability for writes, so let's try creating an example that is
focussed primarily on writes: a Last.fm clone.

Since Cassandra models the queries of your domain rather than the
data, here's an outline of the queries one does against a scrobble
backend:

Basic Queries:

 * create a User
 * record a User password hash for authentication
 * record Songs listened to per User
 * list last x played Songs per User in reverse chronological order

Friends:

 * record a User following another User
 * list Users a User follows
 * list Users that follows a User

Harder queries:

 * record a Tag on a Song per User
 * record a Tag on an Artist per User
 * record a Tag on an Album per User
 * search by tags on Songs, Artists, or Albums sorted by number of Users who tagged it such.

 * List top tracks per user
 * List top tracks for all Users

