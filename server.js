//Requiring the modules -> It should always be done on the top
const express = require("express");
const ejs = require("ejs"); //View Engine
const path = require("path");
const keyword_extractor = require("keyword-extractor");
const fs = require("fs/promises");
const { readFileSync } = require("fs");
const { type } = require("os");
const { stringify } = require("querystring");
//Creating our server
const app = express();

app.use(express.json());

//Setting Up EJS

app.set("view engine", "ejs");

app.use(express.static(path.join(__dirname, "/pub")));

const PORT = process.env.PORT || 3000;
let tfidr = readFileSync("./Files/tfidr.txt", (encoding = "utf8"));
let title = readFileSync(
  "./Files/Leetcode_problems_title.txt",
  (encoding = "utf8")
);
let link = readFileSync(
  "./Files/Leetcode_problems_link.txt",
  (encoding = "utf8")
);
let keyWord = readFileSync("./Files/keywords.txt", "utf8");

tfidr = tfidr.split(/\n/);
title = title.split(/\n/);
link = link.split(/\n/);
keyWord = keyWord.split(" ");
for (let i = 0; i < 147; i++) {
  tfidr[i] = tfidr[i].split(" ");
}

for (let i = 0; i < 147; i++) {
  tfidr[i] = tfidr[i].map((value) => {
    return Number(value);
  });
}
// GET, POST, PATCH, DELETE

//@GET /
//description: GET request to home page
app.get("/", (req, res) => {
  res.render("index");
});
app.get("/CompleteQ/:id", (req, res) => {
  let ind = req.params.id;
  let filepath = "./Files/problem" + ind.toString() + ".txt";
  let qbody = readFileSync(filepath, "utf8");
  res.render("details", {
    qbody,
    web: link[ind].replace(/[\r\n]/gm, ""),
    qtitle: title[ind]
      .replaceAll(/[0-9]/g, "")
      .replaceAll(".", "")
      .replace(/[\r\n]/gm, ""),
  });
});
app.get("/search", (req, res) => {
  const query = req.query;

  const question = query.question;
  const extraction_res = keyword_extractor.extract(question, {
    language: "english",
    remove_digits: true,
    return_changed_case: true,
    remove_duplicates: false,
  });
  // The below variable is to set the no. of problems we have til now in our dataset
  let nd = 147;
  let nk = 805; // no. of keywords
  let keyInd = [];

  console.log(typeof keyWord);
  // first I will find the index of the keyword which are present in the query from our keyword.txt

  for (let i = 0; i < extraction_res.length; i++) {
    let j = keyWord.indexOf(extraction_res[i]);
    keyInd.push(j);
  }

  const getFrequency = (array) => {
    const map = {};
    array.forEach((item) => {
      if (map[item]) {
        map[item]++;
      } else {
        map[item] = 1;
      }
    });
    return map;
  };
  keyInd = getFrequency(keyInd);
  Object.keys(keyInd).map(function (key, value) {
    keyInd[key] /= nk;
  });
  // now we have created the tf vector for the query now we need to multiply it with our idf vector

  // below we are making our tf vector compaitible to be multiply with idf vector of matrix
  delete keyInd["-1"];
  for (let i = 1; i <= nk; i++) {
    if (i in keyInd == false) {
      Object.defineProperty(keyInd, i, {
        value: 0,
        writable: true,
        enumerable: true,
        configurable: true,
      });
    }
  }

  // const lines = (tfidr.match(/\n/g) || "").length + 1;

  let idr = tfidr[nd];

  idr = idr.split(" ");
  let it = [];
  it = Object.values(keyInd);
  keyInd = Object.values(keyInd);

  // need to convert idr into a array or object in javascript
  idr = idr.map((value) => {
    return Number(value);
  });

  // console.log("idr[0] type:", typeof idr[0]);
  // console.log("tfidr[0][0] type:", typeof tfidr[0][0]);
  // and then I will do the multiplication to the last row of our tfidx.txt file to get the tfidf vector for our query

  // Now we want to use the tfidf matrix present in our database and use that to generate the tfidf vector for the asked query
  let tfidrquery = [];
  tfidrquery = keyInd.map(function (value, index) {
    value *= idr[index];
    return value;
  });

  let result = [];
  // now using that vector we will do the dot product with all of the document tfidf vector present in the database
  for (let i = 0; i < nd; i++) {
    let sum = 0;
    for (let j = 0; j < nk; j++) {
      sum += tfidrquery[j] * tfidr[i][j];
    }
    result.push(sum);
  }
  // now we will  arrange the above result in decreasing order along with their indexes and use the top ten objects from there
  let result1 = [];
  for (let i of result) {
    result1.push(i);
  }
  // console.log(result1)
  let max147 = [];

  result1.sort((a, b) => (a < b ? 1 : a > b ? -1 : 0));
  for (let i = 0; i < nd; i++) {
    max147.push(result1[i]);
  }
  let max10 = max147.filter((c, index) => {
    return max147.indexOf(c) === index;
  });
  let ansIndex = [];

  for (let i = 0; i < 10; i++) {
    ansIndex.push(result.indexOf(max10[i]));
  }

  console.log(ansIndex);
  /// and then we will publish the title of those top 10 results along with their first line

  // now we will need to use these 10 index and get their title

  //TF-IDF ALgo

  setTimeout(() => {
    let arrtitle = [];
    let ansarr = [];
    for (let i = 0; i < 10; i++) {
      arrtitle.push(
        title[ansIndex[i]]
          .replaceAll(/[0-9]/g, "")
          .replaceAll(".", "")
          .replace(/[\r\n]/gm, "")
      );
    }
    let arrFirstLine = [];
    let allFiles = [];
    let arrLink = [];
    // str.replace(/[\r\n]/gm, '')
    for (let i = 0; i < 10; i++) {
      arrLink.push(link[ansIndex[i]].replace(/[\r\n]/gm, ""));
    }
    for (i = 0; i < 10; i++) {
      let firstline;
      let filepath = "./Files/problem" + ansIndex[i].toString() + ".txt";
      let completefile = readFileSync(filepath, (encoding = "utf8"));

      allFiles.push(completefile);
      completefile = completefile.split(/\n/);
      firstline = completefile[0].replace(/[\r\n]/gm, "");
      arrFirstLine.push(firstline);
    }
    // console.log(arrFirstLine);
    // console.log(arrtitle);
    // console.log(arrLink);

    for (let i = 0; i < 10; i++) {
      let firstline = arrFirstLine[i];
      let problmtitle = arrtitle[i];
      let tmpobj = {
        title: problmtitle,
        statement: firstline,
        ind: ansIndex[i],
      };
      ansarr.push(tmpobj);
    }
    // console.log(ansarr);

    res.json(ansarr);
  }, 2000);
});

//Assigning Port to our application
app.listen(PORT, () => {
  console.log("Server is running on port " + PORT);
});
