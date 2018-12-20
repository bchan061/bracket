// Adding stupid question to make answering 2016 questions slightly better.
stupidQuestions = [
  "Recent polls have shown a fifth of Americans can't locate the U.S. on a world map. Why do you think this is?",
  "Why does Chicken of the Sea taste like tuna?",
  "Do the cars in Cars have life insurance or car insurance?",
  "Why is the word abbreviation so long?",
  "If you clap your hands together, do they kill germs?",
  "Which came first, the oyster or the pearl?",
  "If you suddenly came into the possession of 20 tons of Nutella what would you do?",
  "What's the best advice you've ever received for making a sandwich better?",
];

function main() {
  var data = getData();
  createForms(data, 19);
}

function getData() {
  var sheet = SpreadsheetApp.getActiveSheet();
  var data = sheet.getDataRange().getValues();
  return data;
}

function createForms(data, partToStart) {
  var count = partToStart;
  var elapsed = (partToStart - 1) * 100;
  while (elapsed <= data.length) {
    createForm(data, count, elapsed);
    elapsed += 100;
    count += 1;
  }
}

function createForm(data, section, start) {
  var form = FormApp.create('Questions, Part ' + section);
  form.setTitle('2016 Questions: Part ' + section);
  form.setDescription("Good luck");
  for (var i = start; i < data.length && i < start + 100; i++) {
    // Get the row.
    var row = data[i];
    // First column = the title
    var title = row[0];
    // Second column = choice 1
    var choice1 = row[1];
    // Third column = choice 2
    var choice2 = row[2];
    
    form
      .addMultipleChoiceItem()
      .setTitle(title)
      .setChoiceValues([choice1, choice2])
      .setRequired(true);
  }

  var questionNumber = (section - 1);
  if (questionNumber % 3 == 0) {
    var question = Math.floor(questionNumber / 3);
    var questionString = stupidQuestions[question];
    form.addParagraphTextItem().setTitle(questionString);
     
  }
  
  form
    .addParagraphTextItem()
    .setTitle("Comments");
}
