// helper.js
export function formatDate(date) {
    const year = date.getFullYear();
    const month = ('0' + (date.getMonth() + 1)).slice(-2);
    const day = ('0' + date.getDate()).slice(-2);
    const hours = ('0' + date.getHours()).slice(-2);
    const minutes = ('0' + date.getMinutes()).slice(-2);
    const seconds = ('0' + date.getSeconds()).slice(-2);
    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}

export function getYouTubeEmbedUrl(url) {
    const regex = /[?&]v=([^&#]*)/; // Biểu thức chính quy để tách ID video
    const match = url.match(regex); // Tìm kiếm ID trong URL
    const videoId = match ? match[1] : null; // Nếu tìm thấy thì lấy ID, nếu không thì trả về null

    if (videoId) {
        return `https://www.youtube.com/embed/${videoId}`;
    } else {
        return null; // Trường hợp không tìm thấy ID
    }
}

export function extractIdFromSlug(slug) {
    const parts = slug.split('-id-record-');
    if (parts.length === 2) {
        const idRecord = parts[1];
        if (!isNaN(idRecord) && idRecord.trim() !== '') return idRecord;
    }
    this.$router.push({ name: 'CommonNotFound' });
}

export function formatDate2(date) {
    const formattedDate = new Date(date);

    const day = formattedDate.getDate();
    const month = formattedDate.getMonth() + 1;
    const year = formattedDate.getFullYear();

    const formattedDateString = `${day}/${month}/${year}`;

    return formattedDateString;
}

export function removeStringFromFileLink(inputString, fileLink) {
    if(fileLink) return fileLink.replace(inputString, '');
    else return '';
}

export function formatNumber(input) {
    return input.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ".");
}

export function extractFileName(url) {
    if(url) {
        const urlParts = url.split('/'); 
        return urlParts[urlParts.length - 1]; 
    }
}

// export function goto(name) {
//     this.$router.push({ name: 'AccountSetting' }); 
// }
