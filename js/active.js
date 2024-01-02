// 이미지 초기 경로를 저장할 객체 생성
var originalImageSrc = {};

// 초기 이미지 경로 저장
document.querySelectorAll('.img').forEach(function (img) {
    originalImageSrc[img.parentElement.className] = img.src;
});

// 페이지 로드 시 program-manage를 클릭한 것처럼 처리
window.addEventListener('DOMContentLoaded', function () {
    var programManageElement = document.querySelector('.program-manage');
    if (programManageElement) {
        simulateClick(programManageElement);
    }
});

// 모든 요소에 대한 이벤트 리스너 등록
document.querySelector('.side-menuBar').addEventListener('click', function (event) {
    // 클릭된 요소 확인
    var clickedElement = event.target;

    // 클릭된 요소의 부모 요소(.program-manage, .security-record, .settings, .logOut) 찾기
    var parentElement = findParentElement(clickedElement, ['program-manage', 'security-record', 'settings']);

    // 모든 부모 요소 초기화 (기존 내용 삭제)
    // document.querySelector('#main-content').innerHTML = '';

    // 모든 부모 요소 초기화
    var allParentElements = document.querySelectorAll('.program-manage, .security-record, .settings');
    allParentElements.forEach(function (element) {
        element.style.backgroundColor = '';
        var imgElement = element.querySelector('.img');
        var textWrapperElement = element.querySelector('.text-wrapper');
        if (imgElement) {
            // 원래 이미지 경로로 복원
            imgElement.src = originalImageSrc[element.className];
        }

        if (textWrapperElement) {
            textWrapperElement.style.color = '#84828A'; // text-wrapper의 텍스트 색상을 검정색으로 변경
        }

        
    });

    // 만약 부모 요소가 있다면
    if (parentElement) {
        // 클릭 이벤트의 기본 동작 막기
        event.preventDefault();

        // 부모 요소의 배경 색상을 pink로 변경
        parentElement.style.backgroundColor = '#ffeefc';

        // 자식 요소의 img 클래스 변경 (대체 이미지로 교체)
        var imgElement = parentElement.querySelector('.img');
        if (imgElement) {
            imgElement.src = imgElement.getAttribute('data-alt-src');
        }

        // 자식 요소의 text-wrapper의 색상 변경
        var textWrapperElement = parentElement.querySelector('.text-wrapper');
        if (textWrapperElement) {
            textWrapperElement.style.color = '#C234CE'; // text-wrapper의 텍스트 색상을 핑크색으로 변경
        }

        // 메뉴에 따라 외부 HTML 파일 가져와서 삽입
        if (parentElement.classList.contains('program-manage')) {
            // 프로그램 관리 메뉴를 클릭한 경우
            loadHTML('frame2.html');
        } else if (parentElement.classList.contains('security-record')) {
            // 보안 기록 메뉴를 클릭한 경우
            loadHTML('record.html');
        } else if (parentElement.classList.contains('settings')) {        
            // 설정 메뉴를 클릭한 경우
            loadHTML('exception.html');    
        }

    }
});


// 부모 요소를 찾는 함수
function findParentElement(element, classNames) {
    while (element) {
        if (classNames.some(className => element.classList.contains(className))) {
            return element;
        }
        element = element.parentElement;
    }
    return null;
}

// 요소를 클릭한 것처럼 시뮬레이트하는 함수
function simulateClick(element) {
    var clickEvent = new MouseEvent('click', {
        view: window,
        bubbles: true,
        cancelable: true
    });
    element.dispatchEvent(clickEvent);
}

// 외부 HTML 파일을 가져와서 삽입하는 함수
function loadHTML(url) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', url, true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
            var responseHTML = xhr.responseText;
            document.querySelector('#main-content').innerHTML = responseHTML;
        }
    };
    xhr.send();
}


// 폴더 추가, 파일추가, 삭제 버튼 클릭시 alert
function folderpop(){
    alert("vㅡㅡv 폴더추가 ㅋㅋ");
}

function filepop(){
    alert("@.@ 파일추가 ㅎㅎ");
}

function deletepop(){
    alert("삭 ㅋ 제 ㅋ ㅡ..ㅡr ' ");
}