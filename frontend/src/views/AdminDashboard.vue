<template>
  <div>
    <Navbar />
    <br>
    <div class="mybody">
      <b-row>
        <b-col>
          <b-card title="Book Requests" tag="article" style="max-width: 20rem;" class="mb-2">
            <b-card-text>
              Accept/decline new book requests made by users
            </b-card-text>
            <b-button type="submit" v-b-modal.bookrequest variant="primary"
            @click="bookrequests">Check now</b-button>
          </b-card>
          <b-modal id="bookrequest" ref="modal" size="xl" title="Book Requests" hide-footer>
            <b-container class="row row-flex" id="nav-scroller" ref="content"
              style="padding: 2em; position:relative; height:550px;
                overflow-y:scroll; overflow-x: hidden;">
              <div v-if="requests.length==0">
                <p>No new book request at present.</p>
              </div>
              <div v-else>
                <b-row class="justify-content-md-center border border-primary rounded"
                    style="padding: 1em; margin: 15px; height:200px"
                    v-for="req in requests" :key="req.id">
                <div class="col-2">
                  <img :src="req.coverphoto"
                    class="border" height="170px" width="150px">
                </div>
                <div class="col-6" style="padding: 1em;">
                    <b>Book Name: </b>{{req.bookname}}<br>
                    <b>Author Name: </b>{{ req.authorname }}<br>
                    <i>Requested by: </i><br>
                    <b>Username: </b>{{ req.username }}<br>
                    <b>Email: </b>{{  req.email }}<br>
              <b>Requested for</b> {{ req.weeks }} weeks, {{ req.days }} days, {{ req.hrs }} hours,.
                </div>
                <div class="col-4" style="align-content:space-between;">
                    <center><b>Action</b>
                    <br><br>
                    <b-button variant="success" style="margin: 0.5em;"
                    @click="acceptreq(req.id)" >Accept</b-button>
                    <b-button variant="danger" style="margin: 0.5em;"
                    @click="declinereq(req.id)">Decline</b-button>
                  </center>
                </div>
                </b-row>
              </div>
          </b-container>
          </b-modal>
        </b-col>
        <b-col>
          <b-card title="Add Books" tag="article" style="max-width: 20rem;" class="mb-2">
            <b-card-text>
              Add new book to Book Magnet Application
            </b-card-text>
            <b-button type="submit" v-b-modal.addBook variant="primary">
              Add</b-button>
          </b-card>
          <b-modal id="addBook" ref="modal" title="Add Book" hide-footer>
            <form ref="form">
              <label for="bookname">Book Name</label>
              <input type="text" id="bookname" name="bookname" v-model="bookname"
              class="form-control" required><br>
              <label for="authorname">Author Name/s</label>
              <input type="text" id="authorname" name="authorname" v-model="authorname"
              class="form-control"
                required><br>
              <label for="book">Upload Book File</label>
              <b-form-file v-model="selectedFile[0]" class="form-control"
              id="book" plain ref="file1"
                @change="handle(0)" accept=".pdf" required>
              </b-form-file><br>
              <label for="cp">Upload Book Coverphoto</label>
              <b-form-file v-model="selectedFile[1]" class="form-control"
              id="cp" plain ref="file2" @change="handle(1)"
                accept="image/jpeg, image/png" required>
              </b-form-file><br>
              <b-button type="submit" @click.prevent="addBooks" class="form-control">
                Add Book</b-button>
            </form>
          </b-modal>
        </b-col>
        <b-col>
          <b-card title="Add Section" tag="article" style="max-width: 20rem;" class="mb-2">
            <b-card-text>
              Add new section (A book can be assigned to one section only)
            </b-card-text>
            <b-button type="submit" v-b-modal.addSection variant="primary"
            @click="getBooks">Add</b-button>
          </b-card>
          <b-modal id="addSection" ref="modal" title="Add Section" hide-footer>
            <form ref="form">
              <label for="sname">Section Name</label>
              <input type="text" id="sname" name="sname" v-model="sname"
              class="form-control" required><br>
              <label for="descryp">Section Description</label>
              <textarea type="text" id="descryp" name="descryp" v-model="descryp"
              class="form-control" required></textarea> <br>
              <label for="n=booklist">Add books</label>
              <b-form-select v-model="selectedOptions" class="mb-3" multiple>
                <b-form-select-option :value="null" disabled :selected="true">
                  Select all books related to this section</b-form-select-option>
                <b-form-select-option :value=book.id v-for="book in bookslist.filter(
                  (book)=> book.section_id == null)" :key="book.id">
                  "{{ book.bookname }}" By {{ book.authorname }}
                </b-form-select-option>
              </b-form-select>
              <b-button type="submit" @click.prevent="addSection" class="form-control">
                Add Section</b-button>
            </form>
          </b-modal>
        </b-col>
      </b-row>
      <br>
      <br>
      <b-row>
        <b-col>
          <b-card title="Revoke Access" tag="article" style="max-width: 20rem;" class="mb-2">
            <b-card-text>
              Revoke access for one or multiple e-books(s) from the user
            </b-card-text>
            <b-button type="submit" v-b-modal.revokeAccess variant="primary"
            @click="getBooks">Manage</b-button>
          </b-card>
          <b-modal id="revokeAccess" ref="modal" title="Book Revoke" hide-footer size="xl" >
            <b-container class="row row-flex" id="nav-scroller" ref="content"
              style="padding: 2em; position:relative; height:550px;
                overflow-y:scroll; overflow-x: hidden;">
          <div v-if="bookslist.filter((book)=> book.type=='assign').length==0">
                <p>No books to show</p>
              </div>
              <div v-else>
          <b-row class="justify-content-md-center border border-primary rounded"
            style="padding: 1em; margin: 15px; height:200px" :value=book.id
              v-for="book in bookslist.filter((book)=> book.type=='assign')" :key="book.id">
          <div class="col-2">
            <img :src="book.coverphoto"
              class="border" height="170px" width="150px">
          </div>
          <div class="col-6" style="padding: 1em;">
              <b>Book Name: </b>{{book.bookname}}<br>
              <b>Author Name: </b>{{ book.authorname }}<br>
              <b>Availed on: </b>{{ book.doi }}<br>
              <b>Should return by: </b>{{ book.dor }}<br>
              ({{ book.daysleft }} days {{ book.hoursleft }} hours left)
          </div>
          <div class="col-4" style="align-content:space-between;">
              <center><b>Action</b>
              <br><br>
              <b-button variant="danger" style="margin: 0.5em;"
              @click="takeBook(book.id,book.uid)">Recall</b-button>
            </center>
          </div>
          </b-row>
          </div>
          </b-container>
          </b-modal>
        </b-col>
        <b-col>
          <b-card title="Manage Books" tag="article" style="max-width: 20rem;" class="mb-2">
            <b-card-text>
              Edit/delete book attributes like bookname, author name, etc
            </b-card-text>
            <b-button type="submit" v-b-modal.manageBooks variant="primary"
            @click="getBooks">Manage</b-button>
          </b-card>
          <b-modal id="manageBooks" ref="modal" title="Book Management" hide-footer size="xl" >
          <b-container class="row row-flex" id="nav-scroller" ref="content"
              style="padding: 2em; position:relative; height:550px;
                overflow-y:scroll; overflow-x: hidden;">
                <div v-if="bookslist.length==0">
                <p>No books in the library. Add some books now</p>
              </div>
              <div v-else>
          <b-row class="justify-content-md-center border border-primary rounded"
              style="padding: 1em; margin: 15px; height:200px"
              :value=book.id v-for="book in bookslist" :key="book.id">
          <div class="col-2">
            <img :src="book.coverphoto"
              class="border" height="170px" width="150px">
          </div>
          <div class="col-6" style="padding: 1em;">
              <b>Book Name: </b>{{book.bookname}}<br>
              <b>Author Name: </b>{{ book.authorname }}<br>
              <b>Book Status: </b>
              <span v-if="book.type=='req'" style="background-color: yellow;">
                Not Available<br>
              <span style="background-color: white;">
                <b>Requested by: </b>{{book.username}}</span></span>
              <span v-else-if="book.type=='assign'" style="background-color: red;">
                Not Available<br>
              <span style="background-color: white;">
                <b>Availed by: </b>{{book.username}}</span></span>
              <span v-else-if="book.type=='free'" style="background-color: green;">
                Available</span>
          </div>
          <div class="col-4" style="align-content:space-between;">
              <center><b>Action</b>
              <br><br>
              <b-button type="submit" v-b-modal.editBook @click="getBook(book.id)"
              variant="success" style="margin: 0.5em;">Edit</b-button>
              <b-button variant="danger" style="margin: 0.5em;"
              @click="deleteBook(book.id)">Delete</b-button>
            </center>
          </div>
          </b-row>
          </div>
          </b-container>
          </b-modal>
          <b-modal id="editBook" ref="modal" title="Edit Book" hide-footer size="xl"
          hide-header-close no-close-on-esc @hidden="resetData">
            <form ref="form">
              <label for="bookname">Book Name</label>
              <input type="text" id="bookname" name="bookname" v-model="bookname"
              class="form-control" required><br>
              <label for="authorname">Author Name/s</label>
              <input type="text" id="authorname" name="authorname" v-model="authorname"
              class="form-control" required><br>
              <label for="book">Upload Book File</label>
              <b-form-file v-model="selectedFile[0]" class="form-control"
              id="book" plain ref="file1"
                @change="handle(0)" accept=".pdf" required>
              </b-form-file><br>
              <label for="cp">Upload Book Coverphoto</label>
              <b-form-file v-model="selectedFile[1]" class="form-control"
              id="cp" plain ref="file2" @change="handle(1)"
                accept="image/jpeg, image/png" required>
              </b-form-file><br><p>*all the fields are mandatory</p>
              <b-button type="submit" @click.prevent="editBooks(editbook[0].id)"
                class="form-control" style="margin: 0.5em 0;">Edit Book</b-button>
              <b-button @click="resetData" class="form-control"
                style="margin: 0.5em 0;" variant="danger">Cancel</b-button>
            </form>
          </b-modal>
        </b-col>
        <b-col>
          <b-card title="Manage Section" tag="article" style="max-width: 20rem;" class="mb-2">
            <b-card-text>
              Edit/delete section attributes like sectionname, books, etc
            </b-card-text>
            <b-button type="submit" v-b-modal.manageSection variant="primary"
            @click='getSections'>Manage</b-button>
          </b-card>
          <b-modal id="manageSection" ref="modal" title="Section Mangement" hide-footer size="xl">
            <b-container class="row row-flex" id="nav-scroller" ref="content"
              style="padding: 2em; position:relative; height:550px;
                overflow-y:scroll; overflow-x: hidden;">
                <div v-if="sectionlist.length==0">
                <p>No section to show. Add some sections now</p>
              </div>
              <div v-else>
                <b-row class="justify-content-md-center border border-primary rounded"
                  style="padding: 1em; margin: 15px; height:200px"
                  :value=section.id v-for="section in sectionlist" :key="section.id">
                  <div class="col-6" style="padding: 1em;">
                    <b>Section Name: </b>{{ section.s_name }}<br>
                    <b>Description: </b>{{ section.description }}<br>
                    <b>Created on: </b>{{ section.doc }}<br>
                    <b>Book Count: </b>{{ section.stored_books.length }}
                  </div>
                  <div class="col-4" style="align-content:space-between;">
                  <center><b>Action</b>
                  <br><br>
                  <b-button variant="success" style="margin: 0.5em;"
                  v-b-modal.editSection @click="getSection(section.id)">Edit</b-button>
                  <b-button variant="danger" style="margin: 0.5em;"
                  @click="deleteSection(section.id)">Delete</b-button>
                  </center>
                  </div>
                </b-row>
                </div>
            </b-container>
          </b-modal>
          <b-modal id="editSection" ref="modal" title="Edit Section" hide-footer
          hide-header-close no-close-on-esc @hidden="resetData" size="xl">
            <form ref="form">
              <label for="sname">Section Name</label>
              <input type="text" id="sname" name="sname" v-model="sname"
              class="form-control" required><br>
              <label for="descryp">Section Description</label>
              <textarea type="text" id="descryp" name="descryp" v-model="descryp"
              class="form-control" required></textarea>
              <br>
              <label for="n=booklist">Add books</label>
              <b-form-select v-model="selectedOptions" class="mb-3" multiple>
                <b-form-select-option :value="null" disabled>
                  Select all books related to this section</b-form-select-option>
                <b-form-select-option :value=book.id v-for="book in bookslist" :key="book.id">
                  "{{ book.bookname }}" By {{ book.authorname }}
                </b-form-select-option>
              </b-form-select>
              <b-button type="submit" @click.prevent="editSections(sid)" class="form-control"
                style="margin: 0.5em 0;">Edit Section</b-button>
              <b-button @click="resetData" class="form-control"
                style="margin: 0.5em 0;" variant="danger">Cancel</b-button>
            </form>
          </b-modal>
        </b-col>
      </b-row>
      <p>for BookIssues csv file, give required dates & click on Download</p>
      <b-form @submit.prevent="download">
        <b-row class="align-items-end">
          <b-col md="5" class="mb-3">
          <b-form-group label="Start Date:" label-for="startdate">
            <b-form-datepicker v-model="startdate" id="startdate" style="border-color:black ;">
            </b-form-datepicker>
          </b-form-group>
          </b-col>
          <b-col md="5" class="mb-3">
            <b-form-group label="End Date:" label-for="enddate">
              <b-form-datepicker v-model="enddate" id="enddate" style="border-color:black ;">
              </b-form-datepicker>
            </b-form-group>
          </b-col>
          <b-col md="2" class="mb-3">
            <b-button type="submit" variant="info" style="margin: 0.5em;">
              Download
            </b-button>
          </b-col>
        </b-row>
    </b-form>
    </div>

  </div>
</template>

<script>
import Navbar from '../components/Navbar.vue';

function json(response) {
  return response.json();
}
export default {
  name: 'AdminDashboard',
  components: {
    Navbar,
  },
  data() {
    return {
      startdate: '',
      enddate: '',
      msg: '',
      bookname: '',
      authorname: '',
      selectedFile: [null, null],
      sname: '',
      descryp: '',
      sid: '',
      bookslist: [],
      sectionlist: [],
      selectedOptions: [],
      requests: [],
      editbook: [],
      editsection: [],
    };
  },
  methods: {
    download() {
      // console.log(this.startdate);
      if (this.startdate === '' || this.enddate === '') {
        alert('Give start & end dates');
        return;
      }
      fetch('http://127.0.0.1:5000/downloaddata', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          'Content-type': 'application/json',
        },
        body: JSON.stringify({
          start_date: this.startdate,
          end_date: this.enddate,
        }),
      }).then((response) => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.blob();
      }).then((blob) => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = 'BookIssueData.csv';
        a.click();
        window.URL.revokeObjectURL(url); // Clean up the URL object
      })
        .catch(() => {
          alert('Something went wrong. Please logout and login again');
        });
    },
    handle(index) {
      console.log(index);
    },
    takeBook(id, uid) {
      fetch('http://127.0.0.1:5000/returnbook', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          'Content-type': 'application/json',
        },
        body: JSON.stringify({
          bookid: id,
          userid: uid,
        }),
      }).then(json)
        .then((data) => {
          if (data.msg === 'Success') {
            alert('Revoke successfull');
            this.getBooks();
          } else {
            alert(data.msg);
          }
        });
    },
    resetData() {
      this.sid = '';
      this.sname = '';
      this.descryp = '';
      this.bookname = '';
      this.authorname = '';
      this.selectedOptions = [];
      this.$refs.modal.hide();
    },
    getBook(id) {
      this.editbook = this.bookslist.filter((book) => {
        if (book.id === id) {
          this.bookname = book.bookname;
          this.authorname = book.authorname;
          return book;
        }
        return null;
      });
    },
    getSection(id) {
      this.editsection = this.sectionlist.filter((sec) => {
        if (sec.id === id) {
          this.sname = sec.s_name;
          this.descryp = sec.description;
          this.sid = id;
          for (let i = 0; i < sec.stored_books.length; i += 1) {
            this.selectedOptions.push(sec.stored_books[i].id);
          }
          this.getBooks();
          return sec;
        }
        return null;
      });
    },
    acceptreq(id) {
      const formdata = new FormData();
      formdata.append('reqid', id);
      formdata.append('type', 1);
      fetch('http://127.0.0.1:5000/requestbook', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
        },
        body: formdata,
      }).then(json)
        .then((data) => {
          if (data.msg === 'Success') {
            console.log('"Hello"');
            this.bookrequests();
          } else {
            alert(data.msg);
          }
        });
    },
    declinereq(id) {
      const formdata = new FormData();
      formdata.append('reqid', id);
      formdata.append('type', 0);
      fetch('http://127.0.0.1:5000/requestbook', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
        },
        body: formdata,
      }).then(json)
        .then((data) => {
          if (data.msg === 'Success') {
            console.log('"Hello"');
            this.bookrequests();
          } else {
            alert(data.msg);
          }
        });
    },
    deleteBook(id) {
      if (window.confirm('Are you sure deleting the book')) {
        const formdata = new FormData();
        formdata.append('bid', id);
        fetch('http://127.0.0.1:5000/removebook', {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          },
          body: formdata,
        }).then(json)
          .then((data) => {
            if (data.msg === 'Success') {
              alert('Book deleted successfully');
              this.getBooks();
            } else {
              alert(data.msg);
            }
          });
      }
    },
    deleteSection(id) {
      if (window.confirm('Are you sure deleting the section')) {
        const formdata = new FormData();
        formdata.append('sid', id);
        fetch('http://127.0.0.1:5000/removesection', {
          method: 'POST',
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          },
          body: formdata,
        }).then(json)
          .then((data) => {
            if (data.msg === 'Success') {
              alert('Section deleted successfully');
              this.getSections();
            } else {
              alert(data.msg);
            }
          });
      }
    },
    editBooks(id) {
      if (!this.selectedFile[0] || !this.selectedFile[1]) {
        alert('Please upload both book file and cover photo.');
        return;
      }
      if (!this.bookname || !this.authorname) {
        alert('Please provide all required fields');
        return;
      }
      const formData = new FormData();
      formData.append('bid', id);
      formData.append('bookname', this.bookname);
      formData.append('authorname', this.authorname);
      this.selectedFile.forEach((file, index) => {
        if (file) {
          formData.append(`file${index + 1}`, file);
        }
      });
      fetch('http://127.0.0.1:5000/editbook', {
        method: 'post',
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
        },
        body: formData,
      }).then(json)
        .then((data) => {
          if (data.msg === 'Success') {
            alert('Book Edited successfully.');
            this.$refs.modal.hide();
            this.bookname = '';
            this.authorname = '';
            this.selectedFile = [null, null];
            this.getBooks();
          } else {
            alert(data.msg);
          }
        }).catch((error) => {
          console.error('Error:', error);
          alert('Failed to edit book.Add again.');
        });
    },
    editSections(id) {
      if (!this.sname || !this.descryp) {
        alert('Please provide all required fields');
        return;
      }
      const formData = new FormData();
      formData.append('sid', id);
      formData.append('s_name', this.sname);
      formData.append('descryp', this.descryp);
      if (this.selectedOptions) {
        formData.append('SelectedOptions', this.selectedOptions);
      }
      fetch('http://127.0.0.1:5000/editsection', {
        method: 'post',
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
        },
        body: formData,
      }).then(json)
        .then((data) => {
          if (data.msg === 'Success') {
            alert('Section Edited successfully.');
            this.$refs.modal.hide();
            this.sname = '';
            this.descryp = '';
            this.selectedOptions = [];
            this.getBooks();
            this.getSections();
          } else {
            alert(data.msg);
          }
        }).catch((error) => {
          console.error('Error:', error);
          alert('Failed to edit book.Add again.');
        });
    },
    addBooks() {
      if (!this.selectedFile[0] || !this.selectedFile[1]) {
        alert('Please upload both book file and cover photo.');
        return;
      }
      if (!this.bookname || !this.authorname) {
        alert('Please provide all required fields');
        return;
      }
      const formData = new FormData();
      formData.append('bookname', this.bookname);
      formData.append('authorname', this.authorname);
      this.selectedFile.forEach((file, index) => {
        if (file) {
          formData.append(`file${index + 1}`, file);
        }
      });
      fetch('http://127.0.0.1:5000/addbook', {
        method: 'post',
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
        },
        body: formData,
      }).then(json)
        .then((data) => {
          if (data.msg === 'Book added successfully') {
            alert('Book added successfully.');
            this.$refs.modal.hide();
            this.bookname = '';
            this.authorname = '';
            this.selectedFile = [null, null];
          } else {
            alert(data.msg);
          }
        }).catch((error) => {
          console.error('Error:', error);
          alert('Failed to add book.Add again.');
        });
    },
    getBooks() {
      fetch('http://127.0.0.1:5000/getbooks', {
        method: 'get',
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
        },
      }).then(json)
        .then((data) => {
          if (data.msg === 'Success') {
            this.bookslist = data.data;
          } else {
            this.$refs.modal.hide();
            alert('Something went wrong');
          }
        });
    },
    getSections() {
      fetch('http://127.0.0.1:5000/getsections', {
        method: 'get',
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
        },
      }).then(json)
        .then((data) => {
          if (data.msg === 'Success') {
            this.sectionlist = data.input_section;
          } else {
            this.$refs.modal.hide();
            alert('Something went wrong');
          }
        });
    },
    bookrequests() {
      fetch('http://127.0.0.1:5000/requestbook', {
        method: 'GET',
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
        },
      }).then(json)
        .then((data) => {
          if (data.msg === 'success') {
            this.requests = data.input_data;
          } else {
            alert(data.msg);
          }
        });
    },
    addSection() {
      if (!this.sname || !this.descryp) {
        alert('Please provide all required fields');
        return;
      }
      const formData = new FormData();
      if (this.selectedOptions) {
        formData.append('SelectedOptions', this.selectedOptions);
      }
      formData.append('Section Name', this.sname);
      formData.append('Descryp', this.descryp);
      fetch('http://127.0.0.1:5000/addsection', {
        method: 'post',
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
        },
        body: formData,
      }).then(json)
        .then((data) => {
          if (data.msg === 'Section added successfully') {
            alert('Section added successfully');
            this.$refs.modal.hide();
            this.sname = '';
            this.descryp = '';
            this.selectedOptions = [null];
          } else {
            alert(data.msg);
          }
        });
    },
  },
};
</script>
<style>
.mybody {
  padding: 0 50px;
}
</style>
