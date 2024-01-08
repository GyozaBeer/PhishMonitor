document.addEventListener('DOMContentLoaded', function() {
    var downloadNrdButton = document.getElementById('downloadNrd');
    if (downloadNrdButton) {
        downloadNrdButton.addEventListener('click', downloadNRD);
    }

    var storeDbButton = document.getElementById('storeDb');
    if (storeDbButton) {
        storeDbButton.addEventListener('click', storeNRDInDB);
    }
});

document.addEventListener('DOMContentLoaded', function() {
    var flashMessages = document.getElementById('flash-messages');
    if (flashMessages) {
        setTimeout(function() {
            flashMessages.style.display = 'none';
        }, 3000); // 3000ミリ秒後に非表示
    }
});

function downloadNRD() {
    fetch('/download_nrd', {
        method: 'POST',
        // 必要に応じてヘッダーやボディを設定
    })
    .then(response => {
        if (!response.ok) { // ステータスコードが200番台以外の場合
            throw new Error('サーバーエラーが発生しました。ステータスコード: ' + response.status);
        }
        return response.json();
    })
    .then(data => {
        if (data.status === 'success') {
            console.log('NRDダウンロード成功');
        } else {
            console.error('NRDダウンロード失敗', data);
        }
    })
    .catch(error => {
        console.error('エラー:', error);
    });
}

function storeNRDInDB() {
    // DB格納APIエンドポイントにリクエストを送信
    fetch('/store_db', {
        method: 'POST',
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            console.log('DB格納成功');
        } else {
            console.error('DB格納失敗');
        }
    })
    .catch(error => {
        console.error('エラー:', error);
    });
}
function confirmLogout() {
    return confirm("ログアウトしますか？");
}

function confirmRemoval() {
    return confirm("このドメインを監視リストから除外してもよろしいですか？");
}

function updateStatus(nrdId) {
    var csrf_token = document.getElementById('csrf_token').value;
    var updateBtn = document.getElementById('updateBtn-' + nrdId);
    var loadingIcon = document.getElementById('loading-' + nrdId);

    updateBtn.classList.add('is-hidden');
    loadingIcon.classList.remove('is-hidden');

    // Fetch APIを使用してAJAXリクエストを送信
    fetch('/check_status', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token
        },
        body: JSON.stringify({ nrdId: nrdId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // ping_statusとcurl_statusの表示を更新
            var pingStatus = document.getElementById('pingStatus-' + nrdId);
            var curlStatus = document.getElementById('curlStatus-' + nrdId);
            var lastChecked = document.getElementById('lastChecked-' + nrdId);

            pingStatus.innerHTML = data.ping_status ? '<span class="icon has-text-success"><i class="fas fa-check-circle"></i></span>' : '<span class="icon has-text-danger"><i class="fas fa-times-circle"></i></span>';
            curlStatus.innerHTML = data.curl_status ? '<span class="icon has-text-success"><i class="fas fa-check-circle"></i></span>' : '<span class="icon has-text-danger"><i class="fas fa-times-circle"></i></span>';
            lastChecked.textContent = data.last_checked; // 応答から新しい確認時刻を設定
            console.log('updating status: ', data);
        } else {
            console.log('Error updating status: ', data);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    })
    .finally(() => {
        // ローディングアイコンを非表示にし、ボタンを表示
        updateBtn.classList.remove('is-hidden');
        loadingIcon.classList.add('is-hidden');
        location.reload()
            });
}

function removeFromWatchlist(nrdId) {
    var csrf_token = document.getElementById('csrf_token').value;
    if (confirm('この監視対象を除外してもよろしいですか？')) {
        // Fetch APIを使用してサーバーに非同期リクエストを送信
        fetch('/remove_from_watchlist', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf_token 
            },
            body: JSON.stringify({ nrdId: nrdId })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // DOMから該当する行を削除
                var row = document.getElementById('row-' + nrdId);
                if (row) {
                    row.remove();
                }
            } else {
                console.log('Error removing NRD: ', data);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
}

function addToWatchlist(nrdId) {
    var csrf_token = document.getElementById('csrf_token').value; // CSRFトークンの取得
    // Fetch APIを使用してサーバーに非同期リクエストを送信
    fetch('/add_to_watchlist', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token 
        },
        body: JSON.stringify({ nrdId: nrdId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // 監視対象追加に成功した場合の処理
            // フラッシュメッセージを表示
            var flashMessagesContainer = document.getElementById('flash-messages-container');
            flashMessagesContainer.innerHTML = `<div class="notification is-success">${data.message}</div>`;
  
            console.log('Added to watchlist: ', data);
            // 必要に応じてDOMの更新などを行う
        } else {
            console.log('Error adding to watchlist: ', data);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}
function removeFromWatchlistSearch(nrdId) {
    var csrf_token = document.getElementById('csrf_token').value;
    if (confirm('この監視対象を除外してもよろしいですか？')) {
        // Fetch APIを使用してサーバーに非同期リクエストを送信
        fetch('/remove_from_watchlist', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf_token 
            },
            body: JSON.stringify({ nrdId: nrdId })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // 監視対象除外に成功した場合、ボタンを「監視対象追加」に変更
                var form = document.getElementById('removeForm-' + nrdId);
                if (form) {
                    form.outerHTML = `
                        <form id="addToWatchlistForm-${nrdId}" onsubmit="return false;">
                            <input type="hidden" name="nrd_id" value="${nrdId}">
                            <button type="button" class="button is-small is-primary" onclick="addToWatchlist('${nrdId}')">監視対象追加</button>
                        </form>`;
                }
            } else {
                console.log('Error removing NRD: ', data);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    }
}

function addToWatchlistSearch(nrdId) {
    var csrf_token = document.getElementById('csrf_token').value; // CSRFトークンの取得
    // Fetch APIを使用してサーバーに非同期リクエストを送信
    fetch('/add_to_watchlist', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token 
        },
        body: JSON.stringify({ nrdId: nrdId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
         // 監視対象追加に成功した場合、ボタンを「監視対象除外」に変更
            var form = document.getElementById('addToWatchlistForm-' + nrdId);
            if (form) {
                form.outerHTML = `
                    <form id="removeForm-${nrdId}" onsubmit="return false;">
                        <input type="hidden" name="nrd_id" value="${nrdId}">
                        <button type="button" class="button is-small is-danger" onclick="removeFromWatchlist('${nrdId}')">監視対象除外</button>
                    </form>`;
            }
            console.log('Added to watchlist: ', data);
            // 必要に応じてDOMの更新などを行う
        } else {
            console.log('Error adding to watchlist: ', data);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function addDomain() {
    var csrf_token = document.getElementById('csrf_token').value; // CSRFトークンの取得
    var domainName = document.querySelector('#addDomainForm input[name="domain_name"]').value;

    // Fetch APIを使用してサーバーに非同期リクエストを送信
    fetch('/add_domain', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrf_token 
        },
        body: JSON.stringify({ domain_name: domainName })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
             // ドメイン追加に成功した場合、テーブルに行を追加
             //　実装申し送り
            console.log('Domain added: ', data);
            // 必要に応じてDOMの更新やフラッシュメッセージの表示
        } else {
            console.log('Error adding domain: ', data);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    })
    .finally(() => {
        location.reload(); // 非同期リクエスト完了後にページをリロード
    });
}