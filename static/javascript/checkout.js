const plus = document.querySelector("#plus-btn")
const minus = document.querySelector("#minus-btn")
const checkoutNum = document.querySelector("#checkoutNum")

function plusClick() {
  let value = checkoutNum.value
  value ++

  if (value > book_remain) {
    alert(`최대 ${book_remain}권 만큼 대여 가능합니다.`)
  } else {
    checkoutNum.value = value
  }
}

function minusClick() {
  let value = checkoutNum.value
  value --

  if (value < 1) {
    alert(`최소 1권 이상 선택해야 합니다.`)
  } else {
    checkoutNum.value = value
  }
}


plus.addEventListener('click', plusClick)
minus.addEventListener('click', minusClick)

