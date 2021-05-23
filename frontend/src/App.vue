<template>
  <h2>Vue + FastAPI + Airtable + Supertrend + Deno</h2>
  <div class="signupForm">
    <form @submit.prevent="submitForm">
      <label for="email">Enter your email address:</label>
      <input
        v-model="userEmail"
        type="email"
        name="email"
        placeholder="Your email..."
        required
      />
      <input type="submit" value="Join waitlist" />
    </form>
  </div>
  <div class="createUserForm">
    <form @submit.prevent="createUser">
      <input
        v-model="userId"
        type="text"
        name="userId"
        placeholder="id"
        required
      />
      <input
        v-model="userName"
        type="text"
        name="userName"
        placeholder="name"
        required
      />
      <input type="submit" value="Create User" />
    </form>
  </div>
  <div class="textarea">
    <textarea
      v-model="textareaContent"
      name=""
      id="content"
      cols="30"
      rows="5"
    ></textarea>
    <button @click="addText">Add Textarea</button>
  </div>
  <div class="getContainer">
    <div class="getRoot">
      <button @click="fetchRoot">Fetch Root</button>
      <div v-show="readRootResponse" class="response">
        readRootReponse: {{ readRootResponse }}
      </div>
    </div>
    <div class="getUsers">
      <button @click="fetchUsers">Fetch Users</button>
      <div v-show="readUsersResponse" class="response">
        readUsersResponse: {{ readUsersResponse }}
      </div>
    </div>
    <div class="getExhange">
      <button @click="fetchExchange">Fetch Exchange</button>
      <div v-show="readExchangeResponse" class="response">
        readExchangeReponse: {{ readExchangeResponse }}
      </div>
    </div>
    <div class="getSupertrend">
      <button @click="fetchSupertrend">Fetch Supertrend</button>
      <div v-show="readSupertrendResponse" class="response">
        readSupertrendResponse: {{ readSupertrendResponse }}
      </div>
    </div>
    <div class="getDeno">
      <button @click="fetchDeno">Fetch Deno</button>
      <!-- <div v-show="readDenoResponse" class="response"> -->
      <!--   readDenoResponse: {{ readDenoResponse }} -->
      <!-- </div> -->
      <!-- NOTE Must use v-html to parse as HTML -->
      <div v-html="readDenoResponse" class="response"></div>
    </div>
    <div class="submitDeno">
      <button @click="submitDenoEmail">Submit Deno Email</button>
      <div v-show="readDenoEmailResponse" class="response">
        readDenoEmailResponse: {{ readDenoEmailResponse }}
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, ref } from "vue";

export default defineComponent({
  name: "App",
  setup() {
    const userEmail = ref<string>("");
    const userId = ref<string>("");
    const userName = ref<string>("");
    const textareaContent = ref<string>("");
    const readRootResponse = ref(null);
    const readExchangeResponse = ref(null);
    const readUsersResponse = ref(null);
    const readSupertrendResponse = ref(null);
    const readDenoResponse = ref<string | null>(null);
    const readDenoEmailResponse = ref<string | null>(null);
    const createUserResponse = ref(null);
    const postResponse = ref(null);

    async function fetchRoot() {
      const response = await fetch("http://localhost:8000/", {
        method: "GET",
      });
      console.log({ response });

      const result = await response.json();
      console.log({ result });
      readRootResponse.value = result;

      return result;
    }

    async function fetchExchange() {
      const response = await fetch("http://localhost:8000/exchange", {
        method: "GET",
      });
      // console.log("fetchExchange:response: ", response);

      // Or, call it result
      const data = await response.json();
      // console.log("fetchExchange:response.json(): ", data);
      readExchangeResponse.value = data;

      return data;
    }

    async function fetchSupertrend() {
      // NOTE I have a separate FastAPI running on port 4000
      // with a /supertrend endpoint
      const response = await fetch("http://localhost:4000/supertrend", {
        method: "GET",
      });
      console.log("fetchSupertrend:response: ", response);
      // Response {type: "cors", url: "http://localhost:4000/supertrend", redirected: false, status: 200, ok: true, …}

      const data = await response.json();
      console.log("fetchSupertrend:response.json(): ", data); // {response: {...}}
      // response:
      //   background: null
      //   body: {data: "{"timestamp":{"0":1613088000000,"1":1613174400000,…:null,"95":null,"96":"Sell","97":null,"98":null}}"}
      //   raw_headers: []
      //   status_code: null

      readSupertrendResponse.value = data;
      return data;
    }

    async function fetchDeno() {
      // NOTE Another separate API server endpoint by Deno!
      // === API returning JSON
      // const response = await fetch("http://localhost:5000/deno", {
      //   method: "GET",
      //   headers: {
      //     "Content-Type": "application/json",
      //   },
      // });
      // console.log("fetchDeno:response: ", response);
      // console.log("fetchDeno:response.body: ," response.body)  // Broken...

      // NOTE If Content-Type = 'text/plain' => response.body = ReadableStream object
      // API returning JSON:
      // NOTE If Content-Type = 'application/json' AND server returns JSON in response.body
      // => THEN you can await response.json() and it will work!
      // const data = await response.json(); // { api: "Deno" }
      // console.log("fetchDeno:response.json(): ", data);  // { api: "Deno"}
      // readDenoResponse.value = data;

      // return data;

      // === API returning HTML:
      // NOTE Must use v-html to parse as HTML
      const response = await fetch("http://localhost:5000/deno", {
        method: "GET",
        headers: {
          "Content-Type": "text/html",
        },
      });
      console.log("fetchDeno:response: ", response);
      // console.log("response.body: ", response.body); // ReadableStream<Uint8Array | null>
      // console.log("response.text: ", response.text); // text() {[native code]}
      // console.log("response.text(): ", response.text()); // Promise {<pending>}

      // Let's await the response.text() method
      const response_html: string = await response.text();
      console.log("await response.text(): ", response_html); // Works! <h3>Deno HTML</h3>
      readDenoResponse.value = response_html;

      return response_html;
    }

    async function addText() {
      const response = await fetch("http://localhost:8000/add", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          content: textareaContent.value,
        }),
      });

      const data = await response.json();
      console.log("addText:data: ", data);
      postResponse.value = data;

      return data;
    }

    async function fetchUsers() {
      const response = await fetch("http://localhost:8000/users", {
        method: "GET",
      });
      console.log({ response });

      // Or, call it result
      const data = await response.json();
      // console.log({ data });
      readUsersResponse.value = data;

      return data;
    }

    async function submitForm() {
      console.log("submitForm");
      console.log(userEmail.value);

      // NOTE The response that comes back is determined by
      // the FastAPI endpoint operation!
      // E.g., Return request.json() or { "result": request, "fruit": banana }, etc.
      const response = await fetch("http://localhost:8000/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: userEmail.value,
        }),
      });

      console.log(response);

      const result = await response.json();
      console.log(result);

      // NOTE 'result' depends on what I return from FastAPI endpoint
      // E.g., If I just return result -> {email: "signup@abc.com"}
      // E.g., If I return a dict { "result": result_json, "a": 1 } -> {result: {...}, a: 1}
      postResponse.value = result;

      return result;
    }

    async function submitDenoEmail() {
      /*
      Fetches /denoemail from DENO API endpoint that returns JSON with email key.
      Then takes the returned JSON object and appends to POST request body
      to FastAPI endpoint, which uses Airtable Client to create new record.
      
      BASICALLY PLAYING 'HOT POTATO' BETWEEN THESE SERVERS.
      */
      // 1. Make GET to Deno API endpoint to retrieve JSON object
      const deno_response = await fetch("http://localhost:5000/denoemail", {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });
      console.log("submitDenoEmail:deno_response: ", deno_response); // Response
      const deno_result = await deno_response.json();
      console.log("submitDenoEmail:await deno_response.json(): ", deno_result); // {email: "emailfromdeno@abc.com"}
      readDenoEmailResponse.value = deno_result;

      // 2. Make POST to FastAPI endpoint with fetched Deno JSON object
      const fastapi_response = await fetch("http://localhost:8000/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: deno_result.email,
        }),
      });

      console.log("submitDenoEmail:fastapi_response: ", fastapi_response);

      const fastapi_result = await fastapi_response.json();
      console.log(
        "submitDenoEmail:await fastapi_response.json(): ",
        fastapi_result
      );

      // NOTE 'result' depends on what I return from FastAPI endpoint
      // E.g., If I just return result -> {email: "signup@abc.com"}
      // E.g., If I return a dict { "result": result_json, "a": 1 } -> {result: {...}, a: 1}
      //postResponse.value = fastapi_result;

      return fastapi_result;
    }

    async function createUser() {
      // Grab input values from the form
      const user = {
        id: userId.value,
        name: userName.value,
      };
      console.log({ user });

      // Make our POST request to our backend API
      const response = await fetch("http://localhost:8000/user", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        // body: JSON.stringify({
        //   // NOTE Can't simply pass user: user. Must pass fields!
        //   id: user.id,
        //   name: user.name,
        // }),
        // Q: Can I just JSON.stringify(user)?
        // A: Yes! It works!
        body: JSON.stringify(user),
      });

      const data = await response.json();

      createUserResponse.value = data;
      console.log("createUserResponse: ", createUserResponse.value);

      return data;
    }

    return {
      fetchRoot,
      fetchExchange,
      fetchUsers,
      fetchSupertrend,
      fetchDeno,
      readRootResponse,
      readExchangeResponse,
      readUsersResponse,
      readSupertrendResponse,
      readDenoResponse,
      readDenoEmailResponse,
      createUserResponse,
      submitForm,
      submitDenoEmail,
      createUser,
      addText,
      postResponse,
      userEmail,
      userId,
      userName,
      textareaContent,
    };
  },
});
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  box-sizing: border-box;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  align-items: center;
}

*,
*:before,
*:after {
  box-sizing: inherit;
}

.signupForm {
  margin: 10px auto;
}

.signupForm form {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 70%;
  margin: 5px auto;
}

.createUserForm {
  margin: 10px auto;
}

.createUserForm form {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 70%;
  margin: 5px auto;
}

.textarea {
  display: flex;
  flex-direction: column;
  width: 400px;
  margin: 10px auto;
}

.getContainer {
  display: flex;
  flex-direction: column;
  width: 400px;
  margin: 10px;
}

.getContainer div {
  height: 150px;
  margin: 10px 0;
  border: 1px solid black;
}

.getContainer .response {
  border: none;
}
</style>
