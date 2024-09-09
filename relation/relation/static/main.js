var nodes;  // 전역 변수로 선언하여 검색에서도 접근 가능하게 함
var network;  // 전역 변수로 선언하여 검색에서도 접근 가능하게 함

// 메뉴 버튼 클릭 시 메뉴를 토글하는 함수
function toggleMenu() {
    const menuItems = document.getElementById('menu-items');
    menuItems.style.display = menuItems.style.display === 'flex' ? 'none' : 'flex';
}

// 새로고침 아이콘 클릭 시 페이지를 새로고침하는 함수
function refreshPage() {
    location.reload();
}

// 네트워크 그래프 생성
function showNetwork() {
    // 서버에서 노드 및 엣지 데이터를 가져옴
    fetch('/get_network_data/')
        .then(response => response.json())
        .then(data => {
            var container = document.getElementById('network');
            nodes = new vis.DataSet(data.nodes.map(node => ({
                id: node.id,
                label: node.label,
                searchkeyword: node.label.toLowerCase(),  // 검색을 위해 사용
                x: node.x * 1000,  // 좌표 값이 작을 수 있으니 적절히 스케일 조정
                y: node.y * 1000,  // 좌표 값 스케일 조정
                fixed: true  // 노드의 위치를 고정
            })));

            var edges = new vis.DataSet(data.edges);

            var options = {
                physics: {
                    enabled: false  // 물리 엔진을 비활성화하여 고정된 좌표 사용
                },
                interaction: {
                    dragNodes: true,  // 노드를 드래그할 수 있도록 설정
                    hover: true,      // 노드에 마우스 올리면 강조
                    selectable: true, // 노드를 선택할 수 있음
                },
                edges: {
                    color: {
                        color: '#FFFFFF',
                        highlight: '#87CEFA',
                        hover: '#FFFFFF'
                    },
                    smooth: {
                        type: 'dynamic',  // 엣지를 부드럽게 보여줌
                    }
                },
                nodes: {
                    shape: 'dot',
                    size: 8,
                    color: {
                        border: '#FFFFFF',
                        background: '#000000',
                        highlight: {
                            border: '#2B7CE9',
                            background: '#D2E5FF'
                        },
                        hover: {
                            border: '#2B7CE9',
                            background: '#D2E5FF'
                        }
                    },
                    font: {
                        color: '#FFFFFF',
                        size: 7,
                        face: 'Arial',
                        align: 'center',
                        strokeWidth: 3,
                        strokeColor: '#000000'
                    },
                    scaling: {
                        min: 10,
                        max: 30
                    },
                    borderWidth: 1
                }
            };

            network = new vis.Network(container, { nodes: nodes, edges: edges }, options);

            // 노드 클릭 시 해당 노드 정보를 사이드 패널에 표시
            network.on("click", function (params) {
                if (params.nodes.length > 0) {
                    var nodeId = params.nodes[0];
                    fetch(`/get_node_data/${nodeId}/`)
                        .then(response => response.json())
                        .then(data => {
                            if (data.error) {
                                console.error(data.error);
                            } else {
                                showSidePanel(data);
                                network.focus(nodeId, {
                                    scale: 2.0,
                                    animation: {
                                        duration: 1000,
                                        easingFunction: "easeInOutQuad"
                                    }
                                });
                            }
                        });
                } else {
                    hideSidePanel();
                    network.fit({
                        animation: {
                            duration: 1000,
                            easingFunction: "easeInOutQuad"
                        }
                    });

                    // 검색창 비우기
                    document.getElementById('search-bar').value = '';  // 검색창 내용 초기화
                }
            });
        });
}

// 페이지 로드 시 네트워크 그래프 생성 함수 호출
window.onload = function () {
    showNetwork();
};

// 사이드 패널을 보여주는 함수
function showSidePanel(nodeData) {
    var sidePanel = document.getElementById('side-panel');
    document.getElementById('panel-title').textContent = nodeData.label;
    document.getElementById('panel-description').textContent = nodeData.mean; // DB에서 가져온 'mean' 값 표시

    sidePanel.style.right = '0'; // 슬라이드 애니메이션을 위한 위치 변경
}


// 사이드 패널을 숨기는 함수
function hideSidePanel() {
    var sidePanel = document.getElementById('side-panel');
    sidePanel.style.right = '-100%'; // 다시 오른쪽으로 슬라이드
}

document.getElementById('search-bar').addEventListener('keyup', function(event) {
    if (event.key === "Enter") {
        var query = this.value.toLowerCase(); // 검색어를 소문자로 변환하여 가져오기
        var exactMatch = nodes.get().find(n => n.searchkeyword === query); // 정확히 일치하는 노드 찾기

        if (exactMatch) {
            focusNode(exactMatch.id); // 일치하는 노드가 있으면 해당 노드로 포커스
        } else {
            alert('해당하는 키워드가 없습니다, 정확하게 입력해주세요!'); // 정확히 일치하는 노드가 없을 경우
        }
    }
});

// 검색창에 입력이 있을 때 유사한 노드 목록을 표시하는 이벤트 처리
document.getElementById('search-bar').addEventListener('input', function() {
    var query = this.value.toLowerCase(); // 입력값을 소문자로 변환하여 검색
    showSuggestions(query);
});

function showSuggestions(query) {
    var suggestionBox = document.getElementById('suggestions');
    suggestionBox.innerHTML = ''; // 기존 목록 초기화

    if (query.length === 0) {
        suggestionBox.style.display = 'none';
        return;
    }

    // 검색어와 일치하는 최대 5개의 노드 찾기
    var matches = nodes.get().filter(n => n.searchkeyword.includes(query)).slice(0, 5);

    if (matches.length > 0) {
        suggestionBox.style.display = 'block';
        matches.forEach(node => {
            var li = document.createElement('li');
            li.textContent = node.label;
            li.onclick = function() {
                focusNode(node.id); // 클릭 시 해당 노드로 포커스
                suggestionBox.style.display = 'none'; // 목록 숨김
                document.getElementById('search-bar').value = node.label; // 검색창에 선택한 노드명 표시
            };
            suggestionBox.appendChild(li);
        });
    } else {
        suggestionBox.style.display = 'none';
    }
}

function focusNode(nodeId) {
    // 노드 선택 시 확대 및 사이드 패널 열기
    fetch(`/get_node_data/${nodeId}/`)
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            console.error(data.error);
        } else {
            // 노드 데이터를 받은 후 사이드 패널에 표시
            showSidePanel(data);

            // 네트워크 상의 노드로 포커스
            network.focus(nodeId, {
                scale: 2.0,
                animation: {
                    duration: 1000,
                    easingFunction: "easeInOutQuad"
                }
            });
        }
    })
    .catch(error => console.error('Error fetching node data:', error));
}
