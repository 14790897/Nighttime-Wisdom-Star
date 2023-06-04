<template>
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
        }
    },
    created() {
      this.socket = io.connect('http://0.0.0.0:5000', {withCredentials: true});
      this.socket.on('login_success', function(data) {
        // After receiving the 'login_success' event, emit a 'join' event with the username.
        this.socket.emit('join', {username: data.username});
      });

      this.socket.on('result', (data) => {
        let data_processed = data   //JSON.parse(data)
        console.warn('data_processed', data_processed);
        const lastMeIndex = this.findIndexFromEnd(this.messages, message => message.text === data_processed.input);
        this.messages.splice(lastMeIndex + 1, 0, { text: data_processed.output, sender: 'bot' });
      });
      this.$http.get('/api/history', { withCredentials: true })
      .then(response => {
        this.messages = response.data.history;
      })
      .catch(error => {
        if (error.response && error.response.status === 401) {
          this.errorMessage = error.response.data.message;
        }
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
  
</style>

  