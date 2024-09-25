document.addEventListener('DOMContentLoaded', function() {
    // ดึงข้อมูลจากเซิร์ฟเวอร์เมื่อหน้าเว็บโหลดเสร็จ
    fetch('/data')
        .then(response => response.json())
        .then(data => {
            // แสดงข้อมูลในหน้าเว็บ
            document.getElementById('message').textContent = data.message;
            document.getElementById('number').textContent = `Number: ${data.number}`;
        })
        .catch(error => {
            console.error('Error:', error);
        });
});
