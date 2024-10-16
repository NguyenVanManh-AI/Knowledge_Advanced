// Folder
describe('Folder | Create Folder', () => {
	beforeEach(() => {
		cy.visit('http://localhost:8080/login');
		cy.get('input[name="email"]').clear().type('admin@gmail.com'); // Nhập email
		cy.get('input[name="password"]').clear().type('admin'); // Nhập mật khẩu
		cy.get('#login_button').click(); // Click nút đăng nhập
		cy.visit('http://localhost:8080/dashboard/manage-folder');
	});

	it('should open the create folder modal', () => {
		// Kiểm tra nút mở modal có tồn tại và click vào
		cy.get('button[data-target="#addRecord"]').should('be.visible').click();

		// Kiểm tra xem modal "Add Folder" đã mở hay chưa
		cy.get('#addRecord').should('be.visible');
	});

	it('should show validation error when folder name is empty', () => {
		// Mở modal thêm thư mục
		cy.get('button[data-target="#addRecord"]').click();

		// Click nút "Add" mà không nhập tên thư mục
		cy.get('#folder_add_button').click();

		// Kiểm tra xem có thông báo lỗi hay không
		cy.get('#add_folder_errors_name').should('contain', 'Folder name cannot be empty !');
	});

	it('should create a new folder successfully', () => {
		// Mở modal thêm thư mục
		cy.get('button[data-target="#addRecord"]').click();

		// // Nhập tên thư mục mới
		const newFolderName = 'New Name Folder';
		cy.get('input[name="add_folder_name"]').type(newFolderName); // không nên dùng type do mất thời gian nhập 

		// Gán giá trị trực tiếp cho input
		// cy.get('input[name="folder_name"]').invoke('val', 'New Name').trigger('change');

		// Click nút "Add"
		cy.get('#folder_add_button').click();

		// Kiểm tra xem modal đã đóng chưa
		cy.get('#addRecord').should('not.be.visible');

		// Kiểm tra danh sách thư mục xem có thư mục mới không
		cy.get('#table_body_folder').should('contain', newFolderName);
	});
});


describe('Folder | Update Folder', () => {
	beforeEach(() => {
		cy.visit('http://localhost:8080/login');
		cy.get('input[name="email"]').clear().type('admin@gmail.com'); // Nhập email
		cy.get('input[name="password"]').clear().type('admin'); // Nhập mật khẩu
		cy.get('#login_button').click(); // Click nút đăng nhập
		cy.visit('http://localhost:8080/dashboard/manage-folder');
	});

	it('should open the update folder modal', () => {
		// Kiểm tra bảng có chứa ít nhất một bản ghi
		cy.get('#table_body_folder tr').should('have.length.greaterThan', 0);

		// Nhấp vào nút cập nhật của bản ghi đầu tiên
		cy.get('#table_body_folder tr')
			.first()
			.find('.updateRecord')
			.click();

		cy.get('#updateRecord').should('be.visible');
	});

	it('should show validation error when folder name is empty', () => {
		// Kiểm tra bảng có chứa ít nhất một bản ghi
		cy.get('#table_body_folder tr').should('have.length.greaterThan', 0);

		// Nhấp vào nút cập nhật của bản ghi đầu tiên
		cy.get('#table_body_folder tr')
			.first()
			.find('.updateRecord')
			.click();

		// clear input name folder 
		cy.get('#updateRecord input[name="update_folder_name"]').clear();
		cy.get('#folder_save_button').click();
		cy.get('#update_folder_errors_name').should('contain', 'Folder name cannot be empty !');
	});

	it('should update the first folder successfully', () => {
		// Kiểm tra bảng có chứa ít nhất một bản ghi
		cy.get('#table_body_folder tr').should('have.length.greaterThan', 0);

		// Nhấp vào nút cập nhật của bản ghi đầu tiên
		cy.get('#table_body_folder tr')
			.first()
			.find('.updateRecord')
			.click();

		// Kiểm tra modal cập nhật hiện ra
		cy.get('#updateRecord').should('be.visible');

		// Cập nhật tên mới cho folder
		const newFolderName = 'Updated Folder Name';
		// cy.get('#updateRecord input[name="update_folder_name"]').clear().type(newFolderName); // type  
		cy.get('#updateRecord input[name="update_folder_name"]').clear().invoke('val', newFolderName).trigger('input'); 
		// => gán và lưu ý là thêm trigger('input') để trong vuejs nhận ra sử thay đổi input để gọi v-model 

		// Lưu các thay đổi
		cy.get('#updateRecord #folder_save_button').click();

		// Kiểm tra xem modal đã đóng chưa
		cy.get('#updateRecord').should('not.be.visible');

		// Kiểm tra xem tên folder đã được cập nhật trong bảng
		cy.get('#table_body_folder tr')
			.first()
			.find('td:nth-child(3)') // Cột thứ 3 là tên folder
			.should('contain.text', newFolderName);
	});
});

describe('Folder | Delete Folder', () => {
	beforeEach(() => {
		cy.visit('http://localhost:8080/login');
		cy.get('input[name="email"]').clear().type('admin@gmail.com'); // Nhập email
		cy.get('input[name="password"]').clear().type('admin'); // Nhập mật khẩu
		cy.get('#login_button').click(); // Click nút đăng nhập
		cy.visit('http://localhost:8080/dashboard/manage-folder');
	});

	it('should open the delete folder modal', () => {
		// Kiểm tra bảng có chứa ít nhất một bản ghi
		cy.get('#table_body_folder tr').should('have.length.greaterThan', 0);

		// Nhấp vào nút xóa của bản ghi đầu tiên
		cy.get('#table_body_folder tr')
			.first()
			.find('.deleteRecord')
			.click();

		cy.get('#deleteRecord').should('be.visible');
	});

	it('should delete the first folder successfully', () => { 
		// Kiểm tra bảng có chứa ít nhất một bản ghi
		cy.get('#table_body_folder tr').should('have.length.greaterThan', 0);
	
		// Lưu ID của bản ghi đầu tiên để kiểm tra sau khi xóa
		let folderId;
		cy.get('#table_body_folder tr')
		  .first()
		  .find('td:nth-child(2)') // Giả sử cột đầu tiên chứa ID của thư mục
		  .invoke('text')
		  .then((id) => {
			  folderId = id.trim();
		  });
	
		// Nhấp vào nút xóa của bản ghi đầu tiên
		cy.get('#table_body_folder tr')
		  .first()
		  .find('.deleteRecord')
		  .click();
	
		// Kiểm tra modal xóa hiện ra
		cy.get('#deleteRecord').should('be.visible');
	
		cy.wait(50); //+++ FIX BUG : 
		// cần phải thêm gì đó GIỮA HAI HÀNH ĐỘNG cy.get('#deleteRecord').should('be.visible'); và cy.get('#deleteRecord #folder_delete_button').click();
		// nếu không sẽ lỗi 

		// Lưu các thay đổi
		cy.get('#deleteRecord #folder_delete_button').click();
	
		// Kiểm tra xem modal đã đóng chưa
		cy.get('#deleteRecord').should('not.be.visible');
	
		// Do sắp xếp giảm dần theo ID nên luôn luôn đảm bảo ID này sẽ là ID lớn nhất nên sẽ không có tình trạng 
		// xóa id = 9 mà kiểm tra id = 19 vẫn còn trong table nên sinh ra test lỗi 
		// Kiểm tra xem thư mục đã bị xóa bằng cách xác nhận ID không còn tồn tại trong bảng
		cy.get('#table_body_folder tr')
		  .should('not.contain', folderId);
	});
	
});

describe('Folder | Search Sort Pagination', () => {
	beforeEach(() => {
		cy.visit('http://localhost:8080/login');
		cy.get('input[name="email"]').clear().type('admin@gmail.com'); // Nhập email
		cy.get('input[name="password"]').clear().type('admin'); // Nhập mật khẩu
		cy.get('#login_button').click(); // Click nút đăng nhập
		cy.visit('http://localhost:8080/dashboard/manage-folder');
	});

	it('should update the number of records displayed per page', () => {
		// Chọn giá trị '10' trong dropdown 'per_page'
		cy.get('#folder_per_page').select('10');
		
		// Kiểm tra xem có đúng 10 bản ghi trong bảng không
		cy.get('#table_body_folder tr').should('have.length', 10);
	
		// Chọn giá trị '20' trong dropdown 'per_page'
		cy.get('#folder_per_page').select('20');
	
		// Kiểm tra xem có đúng 20 bản ghi trong bảng không
		cy.get('#table_body_folder tr').should('have.length', 20);
	});

	it('should sort the records by the selected field', () => {
		// Chọn 'Name' trong dropdown 'sort_by'
		cy.get('#folder_sort_by').select('name');
	
		// Kiểm tra xem cột đầu tiên có được sắp xếp theo tên không
		cy.get('#table_body_folder tr td:nth-child(3)').then(($cells) => {
			const textValues = $cells.map((i, el) => Cypress.$(el).text()).get();
			const sortedValues = [...textValues].sort().reverse(); // Sắp xếp theo thứ tự giảm dần
			expect(textValues).to.deep.equal(sortedValues);
		});
	});

	it('should filter the table based on the search input', () => {
		// Thêm mới folder trước khi search 
		cy.get('button[data-target="#addRecord"]').click();
		const newFolderName = 'Test Search New Name Folder';
		cy.get('input[name="add_folder_name"]').invoke('val', newFolderName).trigger('input');
		cy.get('#folder_add_button').click();

		cy.visit('http://localhost:8080/dashboard/manage-folder'); // đi đến lại manage-folder cho modal không tự đóng 
		// Nhập từ khóa tìm kiếm vào ô tìm kiếm
		const searchText = newFolderName;
		// cy.get('#folder_input_search').type(searchText);
		cy.get('#folder_input_search').invoke('val', searchText).trigger('input');
		
		// Đợi một chút để cập nhật kết quả tìm kiếm
		cy.wait(500);
		
		// Kiểm tra xem bảng chỉ hiển thị các bản ghi chứa từ khóa tìm kiếm
		cy.get('#table_body_folder tr').each(($row) => {
			cy.wrap($row).find('td:nth-child(3)').should('contain.text', searchText);
		});
		
		// Xóa từ khóa và kiểm tra lại toàn bộ bảng
		cy.get('#folder_input_search').clear().trigger('input');
		
		// Đợi một chút để cập nhật lại kết quả
		cy.wait(500);
		
		// Kiểm tra lại bảng sau khi đã xóa từ khóa tìm kiếm
		// trả về như cũ là bảng không rỗng và có ít nhất một bản ghi hiển thị.
		cy.get('#table_body_folder tr').should('have.length.greaterThan', 0);
	});

	it('should not find any folders when searching with a non-existent name', () => {
		const nonExistentSearchText = 'NonExistentFolderName12345';
		cy.get('#folder_input_search').invoke('val', nonExistentSearchText).trigger('input');
		cy.wait(500);
		
		// Kiểm tra bảng không có bản ghi nào hiển thị
		cy.get('#table_body_folder tr').should('have.length', 0);
		
		// Xóa từ khóa tìm kiếm và kiểm tra lại toàn bộ bảng
		cy.get('#folder_input_search').clear().trigger('input');
		
		// Đợi một chút để cập nhật lại kết quả
		cy.wait(500);

		cy.get('#table_body_folder tr').should('have.length.greaterThan', 0);
	});
	
});

// // File
// describe('File | Create Folder', () => {
// 	beforeEach(() => {
// 		cy.visit('http://localhost:8080/login');
// 		cy.get('input[name="email"]').clear().type('admin@gmail.com'); // Nhập email
// 		cy.get('input[name="password"]').clear().type('admin'); // Nhập mật khẩu
// 		cy.get('#login_button').click(); // Click nút đăng nhập
// 		cy.visit('http://localhost:8080/dashboard/manage-folder');
// 	});

// 	it('should open the create folder modal', () => {
// 		// Kiểm tra nút mở modal có tồn tại và click vào
// 		cy.get('button[data-target="#addRecord"]').should('be.visible').click();

// 		// Kiểm tra xem modal "Add Folder" đã mở hay chưa
// 		cy.get('#addRecord').should('be.visible');
// 	});

// 	it('should show validation error when folder name is empty', () => {
// 		// Mở modal thêm thư mục
// 		cy.get('button[data-target="#addRecord"]').click();

// 		// Click nút "Add" mà không nhập tên thư mục
// 		cy.get('#folder_add_button').click();

// 		// Kiểm tra xem có thông báo lỗi hay không
// 		cy.get('#add_folder_errors_name').should('contain', 'Folder name cannot be empty !');
// 	});

// 	it('should create a new folder successfully', () => {
// 		// Mở modal thêm thư mục
// 		cy.get('button[data-target="#addRecord"]').click();

// 		// // Nhập tên thư mục mới
// 		const newFolderName = 'New Name Folder';
// 		cy.get('input[name="add_folder_name"]').type(newFolderName); // không nên dùng type do mất thời gian nhập 

// 		// Gán giá trị trực tiếp cho input
// 		// cy.get('input[name="folder_name"]').invoke('val', 'New Name').trigger('change');

// 		// Click nút "Add"
// 		cy.get('#folder_add_button').click();

// 		// Kiểm tra xem modal đã đóng chưa
// 		cy.get('#addRecord').should('not.be.visible');

// 		// Kiểm tra danh sách thư mục xem có thư mục mới không
// 		cy.get('#table_body_folder').should('contain', newFolderName);
// 	});
// });


// describe('File | Update Folder', () => {
// 	beforeEach(() => {
// 		cy.visit('http://localhost:8080/login');
// 		cy.get('input[name="email"]').clear().type('admin@gmail.com'); // Nhập email
// 		cy.get('input[name="password"]').clear().type('admin'); // Nhập mật khẩu
// 		cy.get('#login_button').click(); // Click nút đăng nhập
// 		cy.visit('http://localhost:8080/dashboard/manage-folder');
// 	});

// 	it('should open the update folder modal', () => {
// 		// Kiểm tra bảng có chứa ít nhất một bản ghi
// 		cy.get('#table_body_folder tr').should('have.length.greaterThan', 0);

// 		// Nhấp vào nút cập nhật của bản ghi đầu tiên
// 		cy.get('#table_body_folder tr')
// 			.first()
// 			.find('.updateRecord')
// 			.click();

// 		cy.get('#updateRecord').should('be.visible');
// 	});

// 	it('should show validation error when folder name is empty', () => {
// 		// Kiểm tra bảng có chứa ít nhất một bản ghi
// 		cy.get('#table_body_folder tr').should('have.length.greaterThan', 0);

// 		// Nhấp vào nút cập nhật của bản ghi đầu tiên
// 		cy.get('#table_body_folder tr')
// 			.first()
// 			.find('.updateRecord')
// 			.click();

// 		// clear input name folder 
// 		cy.get('#updateRecord input[name="update_folder_name"]').clear();
// 		cy.get('#folder_save_button').click();
// 		cy.get('#update_folder_errors_name').should('contain', 'Folder name cannot be empty !');
// 	});

// 	it('should update the first folder successfully', () => {
// 		// Kiểm tra bảng có chứa ít nhất một bản ghi
// 		cy.get('#table_body_folder tr').should('have.length.greaterThan', 0);

// 		// Nhấp vào nút cập nhật của bản ghi đầu tiên
// 		cy.get('#table_body_folder tr')
// 			.first()
// 			.find('.updateRecord')
// 			.click();

// 		// Kiểm tra modal cập nhật hiện ra
// 		cy.get('#updateRecord').should('be.visible');

// 		// Cập nhật tên mới cho folder
// 		const newFolderName = 'Updated Folder Name';
// 		// cy.get('#updateRecord input[name="update_folder_name"]').clear().type(newFolderName); // type  
// 		cy.get('#updateRecord input[name="update_folder_name"]').clear().invoke('val', newFolderName).trigger('input'); 
// 		// => gán và lưu ý là thêm trigger('input') để trong vuejs nhận ra sử thay đổi input để gọi v-model 

// 		// Lưu các thay đổi
// 		cy.get('#updateRecord #folder_save_button').click();

// 		// Kiểm tra xem modal đã đóng chưa
// 		cy.get('#updateRecord').should('not.be.visible');

// 		// Kiểm tra xem tên folder đã được cập nhật trong bảng
// 		cy.get('#table_body_folder tr')
// 			.first()
// 			.find('td:nth-child(3)') // Cột thứ 3 là tên folder
// 			.should('contain.text', newFolderName);
// 	});
// });

// describe('File | Delete Folder', () => {
// 	beforeEach(() => {
// 		cy.visit('http://localhost:8080/login');
// 		cy.get('input[name="email"]').clear().type('admin@gmail.com'); // Nhập email
// 		cy.get('input[name="password"]').clear().type('admin'); // Nhập mật khẩu
// 		cy.get('#login_button').click(); // Click nút đăng nhập
// 		cy.visit('http://localhost:8080/dashboard/manage-folder');
// 	});

// 	it('should open the delete folder modal', () => {
// 		// Kiểm tra bảng có chứa ít nhất một bản ghi
// 		cy.get('#table_body_folder tr').should('have.length.greaterThan', 0);

// 		// Nhấp vào nút xóa của bản ghi đầu tiên
// 		cy.get('#table_body_folder tr')
// 			.first()
// 			.find('.deleteRecord')
// 			.click();

// 		cy.get('#deleteRecord').should('be.visible');
// 	});

// 	it('should delete the first folder successfully', () => { 
// 		// Kiểm tra bảng có chứa ít nhất một bản ghi
// 		cy.get('#table_body_folder tr').should('have.length.greaterThan', 0);
	
// 		// Lưu ID của bản ghi đầu tiên để kiểm tra sau khi xóa
// 		let folderId;
// 		cy.get('#table_body_folder tr')
// 		  .first()
// 		  .find('td:nth-child(2)') // Giả sử cột đầu tiên chứa ID của thư mục
// 		  .invoke('text')
// 		  .then((id) => {
// 			  folderId = id.trim();
// 		  });
	
// 		// Nhấp vào nút xóa của bản ghi đầu tiên
// 		cy.get('#table_body_folder tr')
// 		  .first()
// 		  .find('.deleteRecord')
// 		  .click();
	
// 		// Kiểm tra modal xóa hiện ra
// 		cy.get('#deleteRecord').should('be.visible');
	
// 		cy.wait(50); //+++ FIX BUG : 
// 		// cần phải thêm gì đó GIỮA HAI HÀNH ĐỘNG cy.get('#deleteRecord').should('be.visible'); và cy.get('#deleteRecord #folder_delete_button').click();
// 		// nếu không sẽ lỗi 

// 		// Lưu các thay đổi
// 		cy.get('#deleteRecord #folder_delete_button').click();
	
// 		// Kiểm tra xem modal đã đóng chưa
// 		cy.get('#deleteRecord').should('not.be.visible');
	
// 		// Do sắp xếp giảm dần theo ID nên luôn luôn đảm bảo ID này sẽ là ID lớn nhất nên sẽ không có tình trạng 
// 		// xóa id = 9 mà kiểm tra id = 19 vẫn còn trong table nên sinh ra test lỗi 
// 		// Kiểm tra xem thư mục đã bị xóa bằng cách xác nhận ID không còn tồn tại trong bảng
// 		cy.get('#table_body_folder tr')
// 		  .should('not.contain', folderId);
// 	});
	
// });

// describe('File | Search Sort Pagination', () => {
// 	beforeEach(() => {
// 		cy.visit('http://localhost:8080/login');
// 		cy.get('input[name="email"]').clear().type('admin@gmail.com'); // Nhập email
// 		cy.get('input[name="password"]').clear().type('admin'); // Nhập mật khẩu
// 		cy.get('#login_button').click(); // Click nút đăng nhập
// 		cy.visit('http://localhost:8080/dashboard/manage-folder');
// 	});

// 	it('should update the number of records displayed per page', () => {
// 		// Chọn giá trị '10' trong dropdown 'per_page'
// 		cy.get('#folder_per_page').select('10');
		
// 		// Kiểm tra xem có đúng 10 bản ghi trong bảng không
// 		cy.get('#table_body_folder tr').should('have.length', 10);
	
// 		// Chọn giá trị '20' trong dropdown 'per_page'
// 		cy.get('#folder_per_page').select('20');
	
// 		// Kiểm tra xem có đúng 20 bản ghi trong bảng không
// 		cy.get('#table_body_folder tr').should('have.length', 20);
// 	});

// 	it('should sort the records by the selected field', () => {
// 		// Chọn 'Name' trong dropdown 'sort_by'
// 		cy.get('#folder_sort_by').select('name');
	
// 		// Kiểm tra xem cột đầu tiên có được sắp xếp theo tên không
// 		cy.get('#table_body_folder tr td:nth-child(3)').then(($cells) => {
// 			const textValues = $cells.map((i, el) => Cypress.$(el).text()).get();
// 			const sortedValues = [...textValues].sort().reverse(); // Sắp xếp theo thứ tự giảm dần
// 			expect(textValues).to.deep.equal(sortedValues);
// 		});
// 	});
	
// 	it('should filter the table based on the search input', () => {
// 		// Nhập từ khóa tìm kiếm vào ô tìm kiếm
// 		const searchText = 'New Name Folder';
// 		// cy.get('#folder_input_search').type(searchText);
// 		cy.get('#folder_input_search').invoke('val', searchText).trigger('input');
		
// 		// Đợi một chút để cập nhật kết quả tìm kiếm
// 		cy.wait(500);
		
// 		// Kiểm tra xem bảng chỉ hiển thị các bản ghi chứa từ khóa tìm kiếm
// 		cy.get('#table_body_folder tr').each(($row) => {
// 			cy.wrap($row).find('td:nth-child(3)').should('contain.text', searchText);
// 		});
		
// 		// Xóa từ khóa và kiểm tra lại toàn bộ bảng
// 		cy.get('#folder_input_search').clear().trigger('input');
		
// 		// Đợi một chút để cập nhật lại kết quả
// 		cy.wait(500);
		
// 		// Kiểm tra lại bảng sau khi đã xóa từ khóa tìm kiếm
// 		// trả về như cũ là bảng không rỗng và có ít nhất một bản ghi hiển thị.
// 		cy.get('#table_body_folder tr').should('have.length.greaterThan', 0);
// 	});
// });
