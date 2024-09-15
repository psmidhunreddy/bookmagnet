<template>
  <div>
    <nav class="navbar sidebar">
      <ul class="navbar-nav">
        <li class="nav-item" @click="selectMenuItem('books')">
          <p class="nav-link" style="cursor: pointer;">All Books</p>
        </li>
        <li class="nav-item" @click="selectMenuItem('section')">
          <p class="nav-link" style="cursor: pointer;">All Sections</p>
        </li>
        <li class="nav-item" @click="selectMenuItem('yourbooks')">
          <p class="nav-link" style="cursor: pointer;">Your Books</p>
        </li>
        <li class="nav-item" @click="selectMenuItem('pastbooks')">
          <p class="nav-link" style="cursor: pointer;">Past Books</p>
        </li>
        <li class="nav-item" @click="selectMenuItem('profile')">
          <p class="nav-link" style="cursor: pointer;">Profile</p>
        </li>
      </ul>
    </nav>
    <div class="main-content">
      <div v-if="selectedMenuItem === 'books'">
        <div class="row">
          <div class="col-md-8">
              <h1>All Books</h1>
          </div>
          <div class="col-md-4">
              <b-input-group>
                  <b-form-input v-model="searchTerm"></b-form-input>
                  <b-input-group-append>
                      <b-input-group-text>
                          <b-button variant="outline-primary">
                            <b-icon icon="search"
                            @click="search_book();selectMenuItem('book_search_result')"/></b-button>
                      </b-input-group-text>
                  </b-input-group-append>
              </b-input-group>
          </div>
        </div>
        <b-container class="row row-flex" id="nav-scroller"
        ref="content" style="padding: 2em; position:relative; height:450px;
          overflow-y:scroll; overflow-x: hidden;">
          <div v-if="bookslist.length==0">
            <p>Sorry!No books in the library at present</p>
          </div>
          <div v-else>
          <b-row class="justify-content-md-center rounded"
            style="padding: 1em; margin: 15px; border-style: solid; border-color: #00d4ff;"
            v-for='book in bookslist' :key="book.id">
            <div class="col-2">
              <img :src="book.b_photo" class="border" height="100px" width="100px">
            </div>
            <div class="col-6 align-self-start" style="padding: 1em;">
              <b>Book Name: </b>{{ book.bookname }}<br>
              <b>Author Name: </b>{{ book.authorname }}<br>
              <b>Overall Rating : </b>{{ book.rating }}
            </div>
            <div class="col-2">
              <b>Avail Status</b>
              <div v-if="book.avail_status == 1">
                <b-button variant="success" @click="openRequest(book)">Request</b-button>
              </div>
              <div v-else>
                <b-button variant="danger">Not availble</b-button>
              </div>
            </div>
          </b-row>
          </div>
        </b-container>
        <b-modal v-if="openedrequest" id="book" ref="modal"
          title="Book Request" size="xl" hide-footer>
          <b-row class="justify-content-md-center rounded"
            style="padding: 1em; margin: 15px; border-style: solid; border-color: #00d4ff;"
            >
            <div class="col-2">
              <img :src="openedrequest.b_photo" class="border" height="100px" width="100px">
            </div>
            <div class="col-4 align-self-start" style="padding: 1em;">
              <b>Book Name: </b>{{ openedrequest.bookname }}<br>
              <b>Author Name: </b>{{ openedrequest.authorname }}<br>
              <b>Overall Rating : </b>{{ openedrequest.rating }}
            </div>
            <div class="col-6" style="padding: 1em;">
              <center>
              <form @submit.prevent="validateForm(openedrequest.id)" ref="form">
                <div class="form-group">
                    <input type="number" id="access-hours"
                      v-model.number="accessHours" min="0" max="672"><span> Hours,   </span>
                    <input type="number" id="access-days"
                      v-model.number="accessDays" min="0" max="28"><span> Days,  </span>
                    <input type="number" id="access-weeks"
                      v-model.number="accessWeeks" min="0" max="4"><span> Weeks   </span>
                </div>
                <div id="error-message">{{ errorMessage }}</div>
                <br>
                <b-button variant="success" type="submit">Request</b-button>
            </form>
            </center>
            </div>
            </b-row>
        </b-modal>
      </div>
      <div v-else-if="selectedMenuItem === 'section'">
        <div class="row">
          <div class="col-md-8">
              <h1>All Section</h1>
          </div>
          <div class="col-md-4">
              <b-input-group>
                  <b-form-input v-model="searchTerm"></b-form-input>
                  <b-input-group-append>
                      <b-input-group-text>
                          <b-button variant="outline-primary">
                            <b-icon icon="search" @click="search_section();
                            selectMenuItem('section_search_result')"/></b-button>
                      </b-input-group-text>
                  </b-input-group-append>
              </b-input-group>
          </div>
        </div>
        <b-container class="row row-flex" id="nav-scroller"
        ref="content" style="padding: 0em; position:relative; height:450px;
          overflow-y:scroll; overflow-x: hidden;">
          <div v-if="sectionslist.length==0">
            <p>Sorry!! No sections to display.</p>
          </div>
          <div>
            <div class="rounded" style="margin: 1em; border-style: solid;
            border-color: #00d4ff;"
            v-for='section in sectionslist' :key="section.id">
              <b-card :title="section.s_name" :sub-title="section.description">
                <div style="display: flex; padding: 1em; position:relative; height:300px;
              overflow-y:hidden; overflow-x: scroll;">
                  <div v-for="book in section.stored_books" :key="book.id">
                    <div class="square border border-primary rounded" style="margin: 10px;">
                      <img :src=book.b_photo height="150px" width="150px"><br>
                      <b>{{ book.bookname }}</b><br>
                      by <b>{{ book.authorname }}</b>
                    </div>
                  </div>
                </div>
              </b-card>
            </div>
          </div>
        </b-container>
      </div>
      <div v-else-if="selectedMenuItem === 'yourbooks'">
        <div class="row">
          <div class="col-md-8">
            <h1>Your Books</h1>
          </div>
          <div class="col-md-4">
              <b-input-group>
                  <b-form-input v-model="searchTerm"></b-form-input>
                  <b-input-group-append>
                      <b-input-group-text>
                          <b-button variant="outline-primary">
                            <b-icon icon="search"
                            @click="search_book1();selectMenuItem('book_search_result1')"/>
                          </b-button>
                      </b-input-group-text>
                  </b-input-group-append>
              </b-input-group>
          </div>
        </div>
        <b-container class="row row-flex" id="nav-scroller"
        ref="content" style="padding: 2em; position:relative; height:450px;
          overflow-y:scroll; overflow-x: hidden;">
          <div v-if="currentbooks.length==0">
            <p>Hey, looks like your <b>Book Shelf</b> is empty.</p>
            <p>If you have requested some books,
               please wait while the librarian approves the request.</p>
            <p>Thanks for being patient.<i> Happy Reading</i></p>
          </div>
          <div v-else>
          <b-row class="rounded" style="margin: 1em; align-items: center; border-style: solid;
            border-color: #00d4ff; height: 175px"
            v-for='book in currentbooks' :key="book.id">
            <b-col class="col-2">
              <img :src="book.bookdels.b_photo" class="border" height="100px" width="100px">
            </b-col>
            <b-col class="col-3">
              <b>Bookname : </b>{{ book.bookdels.bookname }}<br>
              <b>Author : </b>{{ book.bookdels.authorname }}<br>
              <b>Rating : </b>{{ book.bookdels.rating }}
            </b-col>
            <b-col class="col-4">
              <b>Issued on : </b>{{ book.issue_date }}<br>
              <b>Return by : </b>{{ book.return_date }}
            </b-col>
            <b-col class="col-3">
              <b-button type="submit" @click="openbook(book)"
              variant="info">View Book</b-button><br><br>
              <b-button type="submit" @click="bookreturn(book.bid)"
              variant="danger">Return Book</b-button>
            </b-col>
          </b-row>
          </div>
        </b-container>
        <b-modal v-if="openedbook" id="book" ref="modal" size="xl"
          :title="openedbook.bookdels.bookname" hide-footer>
            <iframe :src="openedbook.bookdels.book_content+'#toolbar=0'"
              scrolling='auto' height='480px' width='100%'></iframe>
              <div>
                <b-button v-b-toggle.collapse-1 variant="primary">Pay to Download</b-button>
                <b-collapse id="collapse-1" class="mt-2">
                  <b-card>
                    <p class="card-text">Price : $00
                      <b-button variant="info"><a style="text-decoration: none;"
                        :href="openedbook.bookdels.book_content" download>
                      Pay Now</a> </b-button>
                      (just click on <b>Pay Now</b> to download, u really have to pay nothing)
                    </p>
                  </b-card>
                </b-collapse>
              </div>
        </b-modal>
      </div>
      <div v-else-if="selectedMenuItem === 'pastbooks'">
        <div class="row">
          <div class="col-md-8">
            <h1>Past Books</h1>
          </div>
          <div class="col-md-4">
              <b-input-group>
                  <b-form-input v-model="searchTerm"></b-form-input>
                  <b-input-group-append>
                      <b-input-group-text>
                          <b-button variant="outline-primary">
                            <b-icon icon="search"
                            @click="search_book2();selectMenuItem('book_search_result2')"/>
                          </b-button>
                      </b-input-group-text>
                  </b-input-group-append>
              </b-input-group>
          </div>
        </div>
        <b-container class="row row-flex" id="nav-scroller"
        ref="content" style="padding: 2em; position:relative; height:450px;
          overflow-y:scroll; overflow-x: hidden;">
          <div v-if="pastbooks.length==0">
            <p>You don't have any past reading</p>
            <p>Visit here once you return a book.</p>
          </div>
          <div v-else>
          <b-row class="rounded" style="margin: 1em; align-items: center; border-style: solid;
            border-color: #00d4ff; height: 175px"
            v-for='book in pastbooks' :key="book.id">
            <b-col class="col-2">
              <img :src="book.bookdels.b_photo" class="border" height="100px" width="100px">
            </b-col>
            <b-col class="col-3">
              <b>Book Name : </b>{{ book.bookdels.bookname }}<br>
              <b>Author Name: </b>{{ book.bookdels.authorname }}<br>
              <b>Overall Rating : </b>{{ book.bookdels.rating }}
            </b-col>
            <b-col class="col-4">
              <b>Issued on : </b>{{ book.issue_date }}<br>
              <b>Returned on : </b>{{ book.return_date }}
            </b-col>
            <b-col class="col-3">
              <b>Give Rating</b><br>
              <b-button type="submit" variant="warning" @click="rate(book.bid)">
                <b-form-rating v-model="rating[book.bid]"></b-form-rating></b-button>
            </b-col>
          </b-row>
          </div>
        </b-container>
      </div>
      <div v-else-if="selectedMenuItem === 'book_search_result'">
        <div class="row">
          <div class="col-md-8">
              <h1>All Books - <i>Search Result</i></h1>
          </div>
          <div class="col-md-4">
              <b-input-group>
                  <b-form-input v-model="searchTerm"></b-form-input>
                  <b-input-group-append>
                      <b-input-group-text>
                          <b-button variant="outline-primary">
                            <b-icon icon="search"
                            @click="search_book();selectMenuItem('book_search_result')"/></b-button>
                      </b-input-group-text>
                  </b-input-group-append>
              </b-input-group>
          </div>
        </div>
        <b-container class="row row-flex" id="nav-scroller"
        ref="content" style="padding: 2em; position:relative; height:450px;
          overflow-y:scroll; overflow-x: hidden;">
          <div v-if="bookssearchlist.length==0">
            <p>Sorry!! No books found.</p>
          </div>
          <div v-else>
          <b-row class="justify-content-md-center rounded"
            style="padding: 1em; margin: 15px; border-style: solid; border-color: #00d4ff;"
            v-for='book in bookssearchlist' :key="book.id">
            <div class="col-2">
              <img :src="book.b_photo" class="border" height="100px" width="100px">
            </div>
            <div class="col-6 align-self-start" style="padding: 1em;">
              <b>Book Name: </b>{{ book.bookname }}<br>
              <b>Author Name: </b>{{ book.authorname }}<br>
              <b>Overall Rating : </b>{{ book.rating }}
            </div>
            <div class="col-2">
              <b>Avail Status</b>
              <div v-if="book.avail_status == 1">
                <b-button variant="success" @click="requestbook(book.id)">Request</b-button>
              </div>
              <div v-else>
                <b-button variant="danger">Not availble</b-button>
              </div>
            </div>
          </b-row>
        </div>
        </b-container>
      </div>
      <div v-else-if="selectedMenuItem === 'book_search_result1'">
        <div class="row">
          <div class="col-md-8">
            <h1>Your Books - <i>Search Result</i></h1>
          </div>
          <div class="col-md-4">
              <b-input-group>
                  <b-form-input v-model="searchTerm"></b-form-input>
                  <b-input-group-append>
                      <b-input-group-text>
                          <b-button variant="outline-primary">
                            <b-icon icon="search"
                            @click="search_book1();selectMenuItem('book_search_result1')"/>
                          </b-button>
                      </b-input-group-text>
                  </b-input-group-append>
              </b-input-group>
          </div>
        </div>
        <b-container class="row row-flex" id="nav-scroller"
        ref="content" style="padding: 2em; position:relative; height:450px;
          overflow-y:scroll; overflow-x: hidden;">
          <div v-if="bookssearchlist1.length==0">
            <p>Sorry!! No books found.</p>
          </div>
          <div v-else>
          <b-row class="rounded" style="margin: 1em; align-items: center; border-style: solid;
            border-color: #00d4ff; height: 175px"
            v-for='book in bookssearchlist1' :key="book.id">
            <b-col class="col-2">
              <img :src="book.bookdels.b_photo" class="border" height="100px" width="100px">
            </b-col>
            <b-col class="col-3">
              <b>Bookname : </b>{{ book.bookdels.bookname }}<br>
              <b>Author : </b>{{ book.bookdels.authorname }}<br>
              <b>Rating : </b>{{ book.bookdels.rating }}
            </b-col>
            <b-col class="col-4">
              <b>Issued on : </b>{{ book.issue_date }}<br>
              <b>Return by : </b>{{ book.return_date }}
            </b-col>
            <b-col class="col-3">
              <b-button type="submit" @click="openbook(book)"
              variant="info">View Book</b-button><br><br>
              <b-button type="submit" @click="bookreturn(book.bid)"
              variant="danger">Return Book</b-button>
            </b-col>
          </b-row>
          </div>
        </b-container>
      </div>
      <div v-else-if="selectedMenuItem === 'book_search_result2'">
        <div class="row">
          <div class="col-md-8">
            <h1>Past Books - <i>Search Result</i></h1>
          </div>
          <div class="col-md-4">
              <b-input-group>
                  <b-form-input v-model="searchTerm"></b-form-input>
                  <b-input-group-append>
                      <b-input-group-text>
                          <b-button variant="outline-primary">
                            <b-icon icon="search"
                            @click="search_book2();selectMenuItem('book_search_result2')"/>
                          </b-button>
                      </b-input-group-text>
                  </b-input-group-append>
              </b-input-group>
          </div>
        </div>
        <b-container class="row row-flex" id="nav-scroller"
        ref="content" style="padding: 2em; position:relative; height:450px;
          overflow-y:scroll; overflow-x: hidden;">
          <div v-if="bookssearchlist2.length==0">
            <p>Sorry!! No books found.</p>
          </div>
          <div v-else>
          <b-row class="rounded" style="margin: 1em; align-items: center; border-style: solid;
            border-color: #00d4ff; height: 175px"
            v-for='book in bookssearchlist2' :key="book.id">
            <b-col class="col-2">
              <img :src="book.bookdels.b_photo" class="border" height="100px" width="100px">
            </b-col>
            <b-col class="col-3">
              <b>Book Name : </b>{{ book.bookdels.bookname }}<br>
              <b>Author Name: </b>{{ book.bookdels.authorname }}<br>
              <b>Overall Rating : </b>{{ book.bookdels.rating }}
            </b-col>
            <b-col class="col-4">
              <b>Issued on : </b>{{ book.issue_date }}<br>
              <b>Returned on : </b>{{ book.return_date }}
            </b-col>
            <b-col class="col-3">
              <b>Give Rating</b><br>
              <b-button type="submit" variant="warning" @click="rate(book.bid)">
                <b-form-rating v-model="rating[book.bid]"></b-form-rating></b-button>
            </b-col>
          </b-row>
          </div>
        </b-container>
      </div>
      <div v-else-if="selectedMenuItem === 'section_search_result'">
        <div class="row">
          <div class="col-md-8">
            <h1>All Sections - <i>Search Result</i></h1>
          </div>
          <div class="col-md-4">
              <b-input-group>
                  <b-form-input v-model="searchTerm"></b-form-input>
                  <b-input-group-append>
                      <b-input-group-text>
                          <b-button variant="outline-primary">
                            <b-icon icon="search" @click="search_section()"/></b-button>
                      </b-input-group-text>
                  </b-input-group-append>
              </b-input-group>
          </div>
        </div>
        <b-container class="row row-flex" id="nav-scroller"
        ref="content" style="padding: 0em; position:relative; height:450px;
          overflow-y:scroll; overflow-x: hidden;">
          <div v-if="sectionsearchlist.length==0">
            <p>Sorry!! No such sections found.</p>
          </div>
          <div v-else>
        <div class="rounded" style="margin: 1em; border-style: solid;
        border-color: #00d4ff;"
        v-for='section in sectionsearchlist' :key="section.id">
          <b-card :title="section.s_name" :sub-title="section.description">
            <div style="display: flex; padding: 1em; position:relative; height:300px;
          overflow-y:hidden; overflow-x: scroll;">
              <div v-for="book in section.stored_books" :key="book.id">
                <div class="square border border-primary rounded" style="margin: 10px;">
                  <img :src=book.b_photo height="150px" width="150px"><br>
                  <b>{{ book.bookname }}</b><br>
                  by <b>{{ book.authorname }}</b>
                </div>
              </div>
            </div>
          </b-card>
        </div>
      </div>
        </b-container>
      </div>
      <div v-else-if="selectedMenuItem === 'profile'">
        <b-container class="row row-flex" id="nav-scroller"
        ref="content" style="padding: 0em; position:relative; height:500px;
          overflow-y:scroll; overflow-x: hidden;">
          <div style="text-align: left;">
            <h1 style="text-align: center">Personel Detials</h1>
            <b-card style=" margin-left: 300px; margin-right: 300px;">
              <b-container>
                <b-row>
                  <b-col>
                    <p>Name</p>
                    <p>Username</p>
                    <p>Email</p>
                    <p>No of books in your shelf</p>
                  </b-col>
                  <b-col cols="6">
                    <p>{{ name }}</p>
                    <p>{{ username }}</p>
                    <p>{{ email }}</p>
                    <p>{{ bcount }}</p>
                    <i style="text-align: right; font-size: small;">
                      &nbsp;&nbsp;&nbsp;
                      *for any discrepancy please contact admin</i>
                  </b-col>
                </b-row>
              </b-container>
            </b-card>
          </div>
          <div style="text-align: left; margin-top: 35px;">
            <h1 style="text-align: center">Password & Security</h1>
            <b-card style=" margin-left: 300px; margin-right: 300px;">
              <b-container>
                <b-row>
                  <b-col>
                    <p style="margin-top: 5px;">Current Password</p><br>
                    <p>New Password</p> <br>
                    <p>Confirm Password</p>
                  </b-col>
                  <b-col cols="6">
                    <b-form-input style="border-color:black;" id="opassword" name="opassword"
                    type="password" v-model="opassword" required>
                    </b-form-input> <br>
                    <b-form-input style="border-color:black;" id="npassword" name="npassword"
                    type="password" v-model="npassword" required>
                    </b-form-input> <br>
                    <b-form-input style="border-color:black;" id="cpassword" name="cpassword"
                    type="password" v-model="cpassword" required>
                    </b-form-input> <br>
                  </b-col>
                </b-row>
              </b-container>
              <center><button id="submit" name="submit" type="submit" class="btn btn-warning"
                    @click.prevent="changePassword">Change Password</button>
                    <div v-if="msg">
                      <p v-if="msg === 'Password change Successful'" style="color: green;">
                        {{ msg }}</p>
                      <p v-else  style="color: red;">{{ msg }}</p>
                    </div>
              </center>
            </b-card>
          </div>
        </b-container>
      </div>
    </div>
  </div>
</template>
<script>
function json(response) {
  return response.json();
}
export default {
  name: 'AllBooks',
  data() {
    return {
      name: '',
      username: '',
      email: '',
      bcount: '',
      msg: '',
      opassword: '',
      npassword: '',
      cpassword: '',
      accessHours: 0,
      accessDays: 0,
      accessWeeks: 0,
      errorMessage: '',
      bookslist: [],
      bookssearchlist: [],
      bookssearchlist1: [],
      bookssearchlist2: [],
      filteredBooks: [],
      sectionslist: [],
      sectionsearchlist: [],
      bookid: 0,
      selectedMenuItem: localStorage.getItem('selectedMenuItem') || 'books',
      currentbooks: [],
      pastbooks: [],
      openedbook: null,
      openedrequest: null,
      rating: [],
      user_rating: JSON.parse(localStorage.getItem('stored_rating')),
      searchTerm: '',
    };
  },
  methods: {
    changePassword() {
      if (this.cpassword !== this.npassword) {
        this.msg = 'Password did not match';
      } else {
        fetch('http://127.0.0.1:5000/changepassword', {
          method: 'post',
          headers: {
            'Content-type': 'application/json',
            Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          },
          body: JSON.stringify({
            oldPass: this.opassword, newPass: this.npassword,
          }),
        }).then(json)
          .then((data) => {
            if (data.msg === 'Password change Successful') {
              this.msg = data.msg;
              this.opassword = '';
              this.npassword = '';
              this.cpassword = '';
            } else this.msg = data.msg;
          });
      }
    },
    validateForm(id) {
      const totalDays = this.accessDays + (this.accessWeeks * 7) + (this.accessHours / 24);
      if (totalDays > 28) {
        this.errorMessage = 'Total access period cannot exceed 28 days.';
      } else {
        this.errorMessage = '';
        this.requestbook(id);
      }
    },
    selectMenuItem(item) {
      localStorage.setItem('selectedMenuItem', item);
      this.selectedMenuItem = localStorage.getItem('selectedMenuItem');
    },
    rate(bid) {
      fetch('http://127.0.0.1:5000/ratebook', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          'Content-type': 'application/json',
        },
        body: JSON.stringify({
          bookid: bid, ratevalue: this.rating[bid],
        }),
      }).then(json)
        .then((data) => {
          if (data.msg === 'Success') {
            localStorage.setItem('stored_rating', JSON.stringify(data.stored_rating));
            for (let i = 0; i < this.user_rating.length; i += 1) {
              this.rating[this.user_rating[i].bid] = this.user_rating[i].value;
            }
            window.location.reload();
          } else {
            alert(data.msg);
          }
        });
    },
    search_section() {
      const searchTerm = this.searchTerm.toLowerCase();
      this.sectionsearchlist = this.sectionslist.filter((section) => section.s_name.toLowerCase()
        .includes(searchTerm) || section.s_name.toLowerCase().includes(searchTerm));
    },
    search_book() {
      const searchTerm = this.searchTerm.toLowerCase();
      this.bookssearchlist = this.bookslist.filter((book) => book.bookname.toLowerCase()
        .includes(searchTerm) || book.authorname.toLowerCase().includes(searchTerm));
    },
    search_book1() {
      alert('dsadsad');
      const searchTerm = this.searchTerm.toLowerCase();
      this.bookssearchlist1 = this.currentbooks.filter((book) => book.bookdels.bookname
        .toLowerCase().includes(searchTerm) || book.authorname.toLowerCase().includes(searchTerm));
    },
    search_book2() {
      alert('dsadsad');
      const searchTerm = this.searchTerm.toLowerCase();
      console.log(this.pastbooks);
      this.bookssearchlist2 = this.pastbooks.filter((book) => book.bookdels.bookname
        .toLowerCase().includes(searchTerm)
          || book.bookdels.authorname.toLowerCase().includes(searchTerm));
    },
    bookreturn(rid) {
      fetch('http://127.0.0.1:5000/returnbook', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          'Content-type': 'application/json',
        },
        body: JSON.stringify({
          bookid: rid,
        }),
      }).then(json)
        .then((data) => {
          if (data.msg === 'Success') {
            alert('success returned');
            window.location.reload();
          } else {
            alert(data.msg);
          }
        });
    },
    openRequest(book) {
      this.openedrequest = book;
      this.$nextTick(() => {
        if (this.$refs.modal) {
          this.$refs.modal.show();
        }
      });
    },
    openbook(book) {
      this.openedbook = book;
      this.$nextTick(() => {
        if (this.$refs.modal) {
          this.$refs.modal.show();
        }
      });
    },
    async requestbook(id) {
      this.bookid = id;
      await fetch('http://127.0.0.1:5000/requestbook', {
        method: 'post',
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          'Content-type': 'application/json',
        },
        body: JSON.stringify({
          bookid: this.bookid,
          hrs: this.accessHours,
          days: this.accessDays,
          weeks: this.accessWeeks,
        }),
      }).then(json)
        .then((data) => {
          if (data.msg === 'Success') {
            console.log('"success"');
            alert('Book is requested! Wait untill it gets approved.');
            window.location.reload();
          } else {
            alert(data.msg);
          }
        });
    },
    async getbooks() {
      await fetch('http://127.0.0.1:5000/getbooks', {
        method: 'get',
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          'Content-type': 'application/json',
        },
      }).then(json)
        .then((data) => {
          if (data.msg === 'Success') {
            this.bookslist = data.data;
          } else {
            alert('Something went wrong');
          }
        });
    },
    async getsections() {
      await fetch('http://127.0.0.1:5000/getsections', {
        method: 'get',
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          'Content-type': 'application/json',
        },
      }).then(json)
        .then((data) => {
          if (data.msg === 'Success') {
            this.sectionslist = data.input_section;
          } else {
            alert('Something went wrong');
          }
        });
    },
    async mycurbooks() {
      await fetch('http://127.0.0.1:5000/curbooks', {
        method: 'get',
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          'Content-type': 'application/json',
        },
      }).then(json)
        .then((data) => {
          if (data.msg === 'Success') {
            this.currentbooks = data.input_curbooks;
            this.pastbooks = data.input_pastbooks;
          } else {
            alert('Something went wrong');
          }
        });
    },
    async myuserdetails() {
      await fetch('http://127.0.0.1:5000/getuser', {
        method: 'get',
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          'Content-type': 'application/json',
        },
      }).then(json)
        .then((data) => {
          if (data.msg === 'Success') {
            this.name = data.name;
            this.username = data.username;
            this.email = data.email;
            this.bcount = data.bcount;
          } else {
            alert('Something went wrong');
          }
        });
    },
  },
  mounted() {
    this.getbooks();
    this.getsections();
    this.mycurbooks();
    this.myuserdetails();
    for (let i = 0; i < this.user_rating.length; i += 1) {
      this.rating[this.user_rating[i].bid] = this.user_rating[i].value;
    }
  },
};
</script>
<style scoped>
.sidebar {
  position: fixed;
  top: 0;
  height: 100%;
  width: 250px;
  padding-left: 3.5rem;
}

.nav-link {
  font-size: 2em;
}

.main-content {
  margin-left: 250px;
  padding: 20px;
}
</style>
