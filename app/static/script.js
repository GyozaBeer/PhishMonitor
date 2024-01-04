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
    return confirm("このNRDを監視リストから除外してもよろしいですか？");
}

function updateStatus(nrdId) {
    var updateBtn = document.getElementById('updateBtn-' + nrdId);
    var loadingIcon = document.getElementById('loading-' + nrdId);

    updateBtn.classList.add('is-hidden');
    loadingIcon.classList.remove('is-hidden');

    // Fetch APIを使用してAJAXリクエストを送信
    fetch('/check_status', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ nrdId: nrdId })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            // ping_statusとcurl_statusの表示を更新
            console.log(data);
        } else {
            console.log(data);
            // エラーハンドリング
        }
    })
    .catch(error => {
        console.error('Error:', error);
        console.log(data);
        // エラーハンドリング
    })
    .finally(() => {
        // ローディングアイコンを非表示にし、ボタンを表示
        updateBtn.classList.remove('is-hidden');
        loadingIcon.classList.add('is-hidden');
        location.reload();
    });

    // AJAXリクエストを送信
    // 例: axios.post('/api/update_status', { nrdId: nrdId })
    // ここにリクエストの成功/失敗に応じた処理を記述

    // デモのために仮のタイムアウトを設定（本番環境では実際のリクエスト処理に置き換える）
    // setTimeout(function() {
    //     // ローディングアイコンを非表示にし、ボタンを表示
    //     updateBtn.classList.remove('is-hidden');
    //     loadingIcon.classList.add('is-hidden');
    // }, 1000); // 1秒後にローディングアイコンを非表示にする
}


// function addToWatchlist(nrdId) {
//     $.ajax({
//         url: "{{ url_for('main.add_to_watchlist_ajax') }}",
//         type: 'POST',
//         data: { nrd_id: nrdId },
//         dataType: 'json',
//         success: function(response) {
//             if (response.status == 'success') {
//                 alert(response.message);  // または他の通知方法
//             } else {
//                 alert(response.message);  // エラーメッセージ
//             }
//         },
//         error: function() {
//             alert('通信エラーが発生しました。');
//         }
//     });
// }
