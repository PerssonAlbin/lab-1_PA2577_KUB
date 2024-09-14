<template>
  <main>
    <h1>Upload a file</h1>
    <form method="post" enctype="multipart/form-data">
      <label for="file">File</label>
      <input id="file" name="file" type="file" />
      <button>Upload</button>
    </form>
  </main>
</template>

<script lang="ts">
import { onMounted } from "vue";
import axios from "axios";

export default {
  name: "IndexPage",

  setup() {
    function handleSubmit(event: any) {
      event.preventDefault();

      const form = event.currentTarget;
      if (!form) return;

      const formData = new FormData(form);

      axios
        .post("http://localhost:3000/upload", formData, {
          headers: {
            "Content-Type": "multipart/form-data",
          },
        })
        .then((response) => {
          console.log("File uploaded successfully:", response.data);
        })
        .catch((error) => {
          console.error("Error uploading file:", error);
        });
    }

    onMounted(() => {
      const form = document.querySelector("form");
      if (!form) return;
      form.addEventListener("submit", handleSubmit);
    });
  },
};
</script>
