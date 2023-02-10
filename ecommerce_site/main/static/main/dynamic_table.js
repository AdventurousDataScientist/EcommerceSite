<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>How to add & remove table rows</title>
    <link
      href="https://fonts.googleapis.com/css2?family=Roboto:wght@100;400&display=swap"
      rel="stylesheet"
    />

    <style>
      body {
        font-family: "Roboto", sans-serif;
      }
      h1 {
        text-align: center;
      }
      table,
      form {
        width: 500px;
        margin: 20px auto;
      }
      table {
        border-collapse: collapse;
      }
      table td,
      table th {
        border: solid 1px black;
      }
      label,
      input {
        display: block;
        margin: 10px 0;
        font-size: 20px;
      }
      button {
        display: block;
      }
    </style>
  </head>
  <body>
    <h1>Dynamically Add & Remove Table Rows</h1>
    <form>
      <div class="input-row">
        <label for="url">Url</label>
        <input type="url" name="url" id="url" />
      </div>
      <div class="input-row">
        <label for="website">Website Name</label>
        <input type="text" name="website" id="website" />
      </div>
      <button>Submit</button>
    </form>
    <table>
      <thead>
        <tr>
          <th>Url</th>
          <th>Website</th>
          <th></th>
        </tr>
      </thead>
      <tbody></tbody>
    </table>
    <script></script>
  </body>
</html>