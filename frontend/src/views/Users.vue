<template>
<div class="p-4">

    <div class="d-flex justify-content-end">
      <div class="mb-4 btn-cluster">
        <button class="btn cbtn-alt btn-sm" data-bs-toggle="modal" data-bs-target="#addUser">
          <i class="bi bi-plus"></i> Add User
        </button>
      </div>
    </div>
    <div>
      <div v-if="users" class="table-res">
        <table class="table table-borderless quote-table pt-5">
          <thead>
            <tr class="border-bottom header">
              <th scope="col">No.</th>
              <th scope="col">Username</th>
              <th scope="col">First Name</th>
              <th scope="col">Last Name</th>
              <th scope="col">Branch</th>
              <th scope="col">Email</th>
              <th scope="col">Last Login</th>
            </tr>
          </thead>
          <tbody class="quote-semi-table">
            <tr class="border-bottom" v-for="(user, index) in users" :key="index">
              <td class="py-4">
                <p>{{ index + 1 + "." }}</p>
              </td>
              <th class="py-4">
                <p>{{ user.username }}</p>
              </th>
              <td class="py-4">
                <p>{{ user.first_name }}</p>
              </td>
  
              <td class="py-4">
                <p>{{ user.last_name }}</p>
              </td>
              <td class="py-4">
                <p>{{ user.branch }}</p>
              </td>
              <td class="py-4">
                <p>
                  {{ user.email.replace(user.email.substring(2, 8), "*******") }}
                </p>
              </td>
              <td class="py-4">
                <p>{{ new Date(user.last_login).toDateString() }}</p>
              </td>
              <td class="py-4">
                <span
                  class="btn btn-sm mr-2 p-2"
                  data-bs-toggle="modal" data-bs-target="#editUser"
                  @click="pushEdit(user)"
                  ><i class="bi bi-pencil-square"></i></span>
              </td>
            </tr>
          </tbody>
        </table>
        <div class="mt-3 text-end pageBtns">
          <button class="btn btn-sm me-2" title="Previous Page">
            <i class="bi bi-arrow-left"></i>
          </button>
          <button class="btn btn-sm" title="Next Page">
            <i class="bi bi-arrow-right"></i>
          </button>
        </div>
      </div>
  
    </div>
    <EditUser :user="sUser"/>
    <AddUser/>
</div>
</template>
<script>
import { useStore } from "vuex";
import { ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import EditUser from "../components/Users/EditUser.vue";
import AddUser from "../components/Users/AddUser.vue";

export default {
  components: {
    EditUser,
    AddUser
},
  setup() {
    const router = useRouter();
    const store = useStore();
    const users = ref();
    const sUser = ref({});

    store.dispatch("fetchAllUsers");
    watch(
      () => [...store.getters.users],
      (newUsers) => {
        users.value = newUsers;
      }
    );

    const pushEdit = (data) => {
      sUser.value = data;
    };

    return { users, pushEdit,sUser };
  },
};
</script>
