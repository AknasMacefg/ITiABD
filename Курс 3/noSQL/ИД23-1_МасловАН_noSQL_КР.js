//1
db.newsfeed.insertOne({
  title: "Открытие в физике",
  theme: "Наука",
  url: "http://primer.com/news_1.txt",
  author: "Petrov",
  vote_count: 10,
  tags: ["физика", "наука"],
  image: {
    url: "http://primer.com/news_1_img.jpg",
    format: "jpg",
    size: 1024
  },
  comments: [{user: "Alex", text: "Хорошая статья!"}]
});

//2
db.newsfeed.insertMany([
  {
    title: "Рост экономики",
    theme: "Экономика",
    url: "http://primer.com/news_2.txt",
    author: "Sidorov",
    vote_count: 50,
    tags: ["экономика"],
    image: {
      url: "http://primer.com/news_2.jpg",
      format: "jpg",
      size: 900
    },
    comments: []
  },
  {
    title: "Кризис рынка",
    theme: "Экономика",
    url: "http://primer.com/news_3.txt",
    author: "USER",
    vote_count: 70,
    tags: ["финансовый", "университет", "кризис"],
    image: {
      url: "http://primer.com/news_3.jpg",
      format: "png",
      size: 1100
    },
    comments: []
  }
]);

//3
load("C:/Users/alexm/Desktop/Рабочая папка/ITiABD/Курс 3/noSQL/news.js");

//4
db.newsfeed.find({ theme: "Наука" }).sort({ vote_count: -1 });

//5
db.newsfeed.find({
  theme: "Экономика и финансы",
  author: "USER"
});


//6
db.newsfeed.distinct("theme");


//7
db.newsfeed.find({tags: "Москва"});

//8
db.newsfeed.find({tags: {$all: ["финансовый", "университет"]}});


//9
db.newsfeed.find({theme: "Наука"}, {title: 1, author: 1, _id: 0});

//10
db.newsfeed.find({author: "USER"}, {comments: 0, _id: 0});

//11
db.newsfeed.find({"image.format": "jpg", "image.size": {$gt: 1000}}, {title: 1, _id: 0});

//12
db.newsfeed.find({"comments.user": "USER"}, {title: 1, _id: 0});

//13
db.newsfeed.find({title: {$regex: "эконом"}}).limit(2);

//14
db.newsfeed.find().sort({_id: 1}).limit(3);

//15
db.newsfeed.find({}, {title: 1, theme: 1, comments: {$slice: ["$comments", 3]}, _id: 0});

//16
db.newsfeed.aggregate([
    {$unwind: "$comments"},
    {$match: {"comments.user": "USER"}},
    {$count: "total_comments_by_user"}
]);

//17
db.newsfeed.aggregate([
    {
        $group: {
            _id: "$theme",
            avg_likes: {$avg: "$vote_count"}
        }
    }
]);

//18
db.newsfeed.aggregate([
    {$match: {theme: "Наука"}},
    {
        $group: {
            _id: "$author",
            count: {$sum: 1}
        }
    }
]);

//19
db.newsfeed.find({theme: {$in: ["Наука", "Экономика"]}, vote_count: {$gt: 100}});

//20
db.newsfeed.aggregate([
    {$group: {_id: "image.format", max_size: {$max: "$image.size"}}}
])

//21
db.newsfeed.find({$expr: {$gte: [{$size: "$comments"}, 3]}});

//22
db.newsfeed.updateMany({theme: "Наука"}, {$inc: {vote_count: 3}});

//23
db.newsfeed.updateOne({title: "Рост экономики"}, {$push: {comments: {user: "USER", text: "Отличная новость!"}}});

//24
db.newsfeed.deleteMany({theme: "Экономика", "comments.user": "USER"});

//25
db.newsfeed.createIndex({theme: 1, author: 1}, {unique: true, name: "theme_author_index"});


