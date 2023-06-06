<template>
    <div class="banner">
      There are still {{ availableChats }} chances to use today, start time: {{ start_time }}, end time: {{ end_time }}.
    </div>
    <div v-if="errorMessage" class="alert alert-danger">
      {{ errorMessage }}
    </div>
    <div class="messages container">
      <div v-for="(message, index) in messages" :key="index" class="message" :class="{'mine': message.sender === 'me'}">
        <span v-text="message.text"></span>
      </div>
      
    </div>
    <form class="mt-3 input-form" @submit.prevent="sendMessage">
        <div class="form-group form-inline">
            <textarea ref="myInput" class="form-control my-input" rows="1" autocomplete="off" v-model="newMessage" @keydown="handleKeydown"></textarea>
          <button class="btn btn-primary">Submit</button>
        </div>
      </form>
</template>
  
  <script>
  import io from 'socket.io-client';
  import { mapState } from 'vuex';
  
  export default {
    data() {
      return {
        newMessage: '',
        messages: [],//JSON.parse('{{ history }}') || []
        csrf_token: '',//{{ csrf_token }}
        errorMessage: '',
        socket: null, // 在这里添加 socket 属性
        availableChats: 0,
        start_time: '',
        end_time: '',
        polling: null,
      };
    },
    computed: {
      ...mapState(['username'])
    },
    methods: {
      sendMessage() {
        if (!this.newMessage.trim()) {
          return; // 如果消息为空，不发送
        }
        else{
          this.$http.post('/api/home', {
            input_data: this.newMessage,
          }, //{
            //headers: {
              // 'X-CSRFToken': this.csrf_token
            //}
          //}
          )
          
          .then(() => {
            console.log(this.messages);
            console.log(this.newMessage)
            this.messages.push({ sender: 'me', text: this.newMessage });
            this.newMessage = '';
            this.$refs.myInput.value = '';
          })
          .catch(error => {
            console.error(error);
            if (error.response && error.response.data && error.response.data.message) {
              console.error("Server responded with message:", error.response.data.message);
              alert(error.response.data.message);
            }
          });
        }
      },
      findIndexFromEnd(array, predicate) {
        for (let i = array.length - 1; i >= 0; i--) {
          if (predicate(array[i], i, array)) {
            return i;
          }
        }
        return -1;
      },
      adjustHeight() {
        const textarea = this.$refs.myInput;
        textarea.style.height = 'auto';
        textarea.style.height = (textarea.scrollHeight) + 'px';
      },
      handleKeydown(e) {
        if(e.keyCode == 13) {
            if(e.shiftKey) {
                var content = this.newMessage;
                var caret = this.getCaret(e.target);
                this.newMessage = content.substring(0, caret) + "\n" + content.substring(caret, content.length);
                e.stopPropagation();
                e.preventDefault();
            } else {
                this.sendMessage();
                e.preventDefault();  // 防止表单默认的提交操作
                console.log('submit');
            }
        }
        },
        getCaret(el) {
            if (el.selectionStart) { 
                return el.selectionStart; 
            } else if (document.selection) { 
                el.focus(); 
                var r = document.selection.createRange(); 
                if (r == null) { 
                    return 0; 
                } 
                var re = el.createTextRange(), 
                rc = re.duplicate(); 
                re.moveToBookmark(r.getBookmark()); 
                rc.setEndPoint('EndToStart', re); 
                return rc.text.length; 
            }  
            return 0; 
        },
        startPolling() {
        this.polling = setInterval(this.getAvailableChats, 5000); // 每5秒请求一次
      },
      stopPolling() {
        clearInterval(this.polling);
        this.polling = null;
      },
      getAvailableChats() {
        this.$http.get('/api/available_chats')
          .then(response => {
            this.availableChats = response.data.availableChats;
          })
          .catch(error => {
            console.error('Error occurred in long polling:', error);
            this.stopPolling(); // 如果发生错误，停止轮询
          });
      },        
    },
    watch: {
    messages() {
      this.$nextTick(() => {
        const container = this.$el.querySelector('.messages');
        container.scrollTop = container.scrollHeight;
        });
      }
    },
    created() {
      // this.socket = io.connect('https://flaskcloud.liuweiqing.top/', {withCredentials: true});
      this.startPolling();
      if (!this.socket) {
        this.socket = io('/', { withCredentials: true });
      }
      this.socket.on('login_success',  () => {
        // After receiving the 'login_success' event, emit a 'join' event with the username.
        this.socket.emit('join');
      });
      this.socket.emit('home_ready');

      this.socket.on('result', (data) => {
        let data_processed = data   //JSON.parse(data)???
        console.warn('data_processed:', data_processed);
        const lastMeIndex = this.findIndexFromEnd(this.messages, message => message.text === data_processed.data.input);
        console.warn('lastMeIndex:', lastMeIndex);
        this.messages.splice(lastMeIndex + 1, 0, { text: data_processed.data.output, sender: 'bot' });
      });
      this.$http.get('/api/history', { withCredentials: true })
      .then(response => {
        this.messages = response.data.history;
      })
      .catch(error => {
        if (error.response && error.response.status === 401) {
          this.errorMessage = this.$t('message.login_required');
        }
      });
      
      this.$http.get('/api/init_chat')
        .then(response => {
          this.start_time = response.data.start_time;
          this.end_time = response.data.end_time;
          this.availableChats = response.data.availableChats;
        }).catch(error => {
          console.error('Init_chat error occurred:', error);
        });
    },
    mounted() {
      this.$refs.myInput.addEventListener('input', this.adjustHeight);
    },
    beforeUnmount() {
      this.$refs.myInput.removeEventListener('input', this.adjustHeight);
      if (this.socket) {
        this.socket.disconnect(); // 在组件卸载前断开连接
      }
      this.stopPolling();
    }
  };
  </script>

  <style scoped>
  body {
  background-color: #f2f2f2;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: Arial, sans-serif;
}

.input-form {
  position: fixed;
  bottom: 0;
  width: 100%;
  background: white;
  padding: 10px;
  box-shadow: 0 -2px 10px rgba(0, 0, 0, 0.1);
}


#app {
  padding-bottom: 50px;  /* 留出足够的空间给输入框 */
}

.messages {
  /* max-width: 600px; */
  margin: 20px auto;
  padding: 20px;
  background-color: white;
  border-radius: 10px;
  box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
}

.message {
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 5px;
  color: white;
}

.message.mine {
  background-color: #c7d3db;
  text-align: right;
}

.message:not(.mine) {
  background-color: #bdb9bf;
}

.input-form .form-group {
  display: flex;
  justify-content: space-between;
  /* justify-content: flex-start; 修改此行 */

  align-items: flex-start;
}

.my-input {
  flex-grow: 1;
  margin-right: 10px;
  resize: none;   /* 禁止用户手动调整大小 */
  overflow: auto; /* 防止滚动条出现 */
}

.input-form .form-group .btn {
  white-space: nowrap;
}
  
.banner {
  width: 100%;
  height: 50px;
  line-height: 50px;
  background-color: #f9f9f9;
  text-align: center;
  color: #333;
}  
</style>

  