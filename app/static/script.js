document.addEventListener('DOMContentLoaded', function() {
    // NRDダウンロードボタンのイベントリスナーを設定
    document.getElementById('downloadNrd').addEventListener('click', function() {
        downloadNRD();
    });

    // DB格納ボタンのイベントリスナーを設定
    document.getElementById('storeDb').addEventListener('click', function() {
        storeNRDInDB();
    });
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

function addToWatchlist(nrdId) {
    $.ajax({
        url: "{{ url_for('main.add_to_watchlist_ajax') }}",
        type: 'POST',
        data: { nrd_id: nrdId },
        dataType: 'json',
        success: function(response) {
            if (response.status == 'success') {
                alert(response.message);  // または他の通知方法
            } else {
                alert(response.message);  // エラーメッセージ
            }
        },
        error: function() {
            alert('通信エラーが発生しました。');
        }
    });
}
