const len = checkout_info.length
const pages = Math.ceil(len / 8)  // 만들어야할 페이지의 개수


// paginationBar 버튼 만들기
const paginationBar = document.querySelector('#pagination')
for (let i=0; i < pages+2; i++) {
  if (i == 0) {
    paginationBar.innerHTML += '<span class="first-btn">&laquo</span>';
  } else if (i == pages+1 ) {
    paginationBar.innerHTML += '<span class="last-btn">&raquo</span>';
  } else {
    paginationBar.innerHTML += `<span class="page-${i} page-btn">${i}</span>`;
  }
}

// 처음 화면 들어갔을때 초기화 부분
const pageBtn = paginationBar.querySelectorAll('.page-btn')
const pageButton = Array.prototype.slice.call(pageBtn)
if (pageButton.length !== 0) {
  pageButton[0].classList.add('activate')
}
const first1 = document.querySelector(`.tr0`)
if (first1) {
  first1.classList.remove('notshow')
}

// 대여목록이 4개가 넘어서 2줄이 되는경우
const first2 = document.querySelector(`.tr1`)
if (first2) {
  first2.classList.remove('notshow')
}

// pagination 중 번호를 클릭했을때 작동하는 코드
function clickHandler(e) {
  const result = pageButton.filter(el => {
    return el.classList.contains('activate')
  })
  // notshow 클래스를 다시 추가해주어야 한다.
  // result를 통해 현재 선택된 테이블을 찾아서 notshow클래스를 추가해준다.
  lastValue = result[0].innerHTML
  const lastTable1 = document.querySelector(`.tr${lastValue*2 - 2}`)
  lastTable1.classList.add('notshow')
  const lastTable2 = document.querySelector(`.tr${lastValue*2 - 1}`)
  if (lastTable2) {
    lastTable2.classList.add('notshow')
  }
  result[0].classList.remove('activate')

  // 현재 클릭한 버튼에 activate클래스를 설정해주고 이에 맞는 테이블에 notshow클래스를 제거해준다.
  e.target.classList.add('activate')
  currentValue = e.target.innerHTML
  const currentTable1 = document.querySelector(`.tr${currentValue*2 - 2}`)
  currentTable1.classList.remove('notshow')
  const currentTable2 = document.querySelector(`.tr${currentValue*2 - 1}`)
  if (currentTable2) {
    currentTable2.classList.remove('notshow')
  }
}

// direction의 값이 1이면 좌측 버튼을 누른 경우
// 그 외는 우측 버튼을 누른 경우이다.
function clickFirstLastBtn(direction) {
  let currentValue
  const result = pageButton.filter(el => {
    return el.classList.contains('activate')
  })

  const lastValue = result[0].innerHTML
  const lastTable1 = document.querySelector(`.tr${lastValue*2 - 2}`)
  lastTable1.classList.add('notshow')
  const lastTable2 = document.querySelector(`.tr${lastValue*2 - 1}`)
  if (lastTable2) {
    lastTable2.classList.add('notshow')
  }
  result[0].classList.remove('activate')

  if (direction == 1) {
    if (lastValue == 1) {
      currentValue = pages
    } else {
      currentValue = lastValue - 1
    }
  } else {
    if (lastValue == pages) {
      currentValue = 1
    } else {
      currentValue = Number(lastValue) + 1
    }
  }

  const currentPage = document.querySelector(`.page-${currentValue}`)
  currentPage.classList.add('activate')
  const currentTable1 = document.querySelector(`.tr${currentValue*2 - 2}`)
  currentTable1.classList.remove('notshow')
  const currentTable2 = document.querySelector(`.tr${currentValue*2 - 1}`)
  if (currentTable2) {
    currentTable2.classList.remove('notshow')
  }
}


// pagination중 왼쪽 화살표 버튼을 클릭했을때 작동하는 코드
function clickFirstBtn(e) {
  clickFirstLastBtn(1)
}


// pagination중 오른쪽 화살표 버튼을 클릭했을때 작동하는 코드
function clickLastBtn(e) {
  clickFirstLastBtn(0)
}


// 숫자 pagination을 클릭했을때 이벤트 설정
pageButton.forEach(element => {
  element.addEventListener('click', clickHandler)
});

const firstBtn = document.querySelector('.first-btn')
// 왼쪽 화살표를 클릭했을때 이벤트 설정
firstBtn.addEventListener('click', clickFirstBtn)

const lastBtn = document.querySelector('.last-btn')
// 오른쪽 화살표를 클릭했을때 이벤트 설정
lastBtn.addEventListener('click', clickLastBtn)