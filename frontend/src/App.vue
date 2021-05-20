<template>
  <h1>Vue + FastAPI</h1>
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
    <div class="getVite">
      <button @click="fetchVite">Fetch Vite</button>
      <div v-show="readViteResponse" class="response">
        readViteReponse: {{ readViteResponse }}
      </div>
    </div>
    <div class="getUsers">
      <button @click="fetchUsers">Fetch Users</button>
      <div v-show="readUsersResponse" class="response">
        readUsersResponse: {{ readUsersResponse }}
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
    const readViteResponse = ref(null);
    const readUsersResponse = ref(null);
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

    async function fetchVite() {
      const response = await fetch("http://localhost:8000/vite", {
        method: "GET",
      });
      console.log({ response });

      // Or, call it result
      const data = await response.json();
      // console.log({ data });
      readViteResponse.value = data;

      return data;
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

      postResponse.value = result;

      return result;
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
      fetchVite,
      fetchUsers,
      readRootResponse,
      readViteResponse,
      readUsersResponse,
      createUserResponse,
      submitForm,
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
  width: 70%;
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
  margin: 10px;
  border: 1px solid black;
}

.getContainer .response {
  border: none;
}
</style>
