// type이 checkbox인 input 태그의 노드들
const rateRadio = document.querySelectorAll('.rate_radio')

rateRadio.forEach((el, idx) => {
  el.addEventListener('click', () => {
    // click한 idx보다 작은 rateRadio의 경우 모두 checked를 true로 바꿔준다.
    // idx보다 더 큰 요소들은 checked를 false로 바꿔준다.

    // 모든 rateRadio의 checked를 바꾸는 과정
    rateRadio.forEach((element, index) => {
      if (index <= idx) {
        element.checked = true
      } else {
        element.checked = false
      }
    })
  })
})

console.log(rateRadio)