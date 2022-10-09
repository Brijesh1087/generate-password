$(document).ready(()=>{
  $("#form").submit((e)=>{
    e.preventDefault()
  })
const func=()=>{
    $.ajax({
      url:location.href+"password",
      type:'GET',
      success:(data)=>{
        console.log(data.password)
        $('#password').val(data.password)
      }
    })
  }
  func()
    $("#generate").click(()=>{
      func()
    })
    // post
    $('#save').click(()=>{
      if($("#name").val().length >= 5){
      $.ajax({
        type:'POST',
        url:location.href+"data",
        contentType: 'application/json;charset=UTF-8',
        data:JSON.stringify({"name":$("#name").val(),'password':$("#password").val(),"csrf":$("#csrf").val()}),
        success:(e)=>{
          console.log(e.return)
        }
      })
    }
    })
    // clipboard
 let  a = document.querySelector("#password")
a.addEventListener("click",()=>{
  a.select()
  navigator.clipboard.writeText(a.value)
  alert("Copy : "+a.value)
})
})

