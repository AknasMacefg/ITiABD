db.newsfeed.insertMany([
  {
    title: "Прорыв в биотехнологиях",
    theme: "Наука",
    url: "http://primer.com/news_1.txt",
    author: "Ivanov",
    vote_count: 120,
    tags: ["биотехнологии", "наука"],
    image: {
      url: "http://primer.com/news_1_img.jpg",
      format: "jpg",
      size: 1500
    },
    comments: [
      { user: "USER", text: "Очень интересно!" },
      { user: "Alex", text: "Ждём продолжения" }
    ]
  },
  {
    title: "Развитие экономики Европы",
    theme: "Экономика и финансы",
    url: "http://primer.com/news_2.txt",
    author: "Petrov",
    vote_count: 85,
    tags: ["экономика", "Европа"],
    image: {
      url: "http://primer.com/news_2_img.jpg",
      format: "jpg",
      size: 980
    },
    comments: [
      { user: "USER", text: "Полезная информация" }
    ]
  },
  {
    title: "Финансовый университет расширяет программы",
    theme: "Экономика и финансы",
    url: "http://primer.com/news_3.txt",
    author: "USER",
    vote_count: 60,
    tags: ["финансовый", "университет"],
    image: {
      url: "http://primer.com/news_3_img.png",
      format: "png",
      size: 1100
    },
    comments: []
  },
  {
    title: "Новые открытия в космосе",
    theme: "Наука",
    url: "http://primer.com/news_4.txt",
    author: "Sidorov",
    vote_count: 200,
    tags: ["космос", "исследования"],
    image: {
      url: "http://primer.com/news_4_img.jpg",
      format: "jpg",
      size: 1300
    },
    comments: [
      { user: "Maria", text: "Потрясающе!" },
      { user: "USER", text: "Люблю космос" },
      { user: "Ivan", text: "Очень познавательно" }
    ]
  },
  {
    title: "Экономический рост в России",
    theme: "Экономика",
    url: "http://primer.com/news_5.txt",
    author: "USER",
    vote_count: 140,
    tags: ["экономика", "Москва"],
    image: {
      url: "http://primer.com/news_5_img.jpg",
      format: "jpg",
      size: 1050
    },
    comments: [
      { user: "Alex", text: "Хороший анализ" },
      { user: "USER", text: "Согласен" }
    ]
  }
]);