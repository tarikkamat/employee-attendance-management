// Leave.js
import API from "./lib/api.js"

const reasonMap = {
    'ANNUAL': 'Yıllık İzin',
    'RELOCATION': 'Taşınma İzni',
    'SICK': 'Hastalık İzni',
    'DEATH_OF_CHILD_OR_SPOUSE': 'Çocuk veya Eşin Vefatı',
    'DEATH_OF_MOM_DAD_OR_SIBLING': 'Anne, Baba veya Kardeşin Vefatı',
    'DEATH_OF_SPOUSE_MOM_DAD_SIBLING': 'Eş, Anne, Baba veya Kardeşin Vefatı',
    'BIRTH_DAY': 'Doğum Günü İzni',
    'SPOUSE_BIRTH_DAY': 'Eşin Doğum Günü İzni',
    'COMPASSIONATE_LEAVE': 'Mazaret İzni',
    'MILITARY_LEAVE': 'Askerlik İzni',
    'MATERNITY_LEAVE': 'Süt İzni',
    'FREE_LEAVE': 'Ücretsiz İzin',
    'MARRIAGE_LEAVE': 'Düğün İzni'
};

const statusMap = {
    'PENDING': {
        text: 'Beklemede',
        class: 'bg-warning-subtle text-warning',
        icon: 'hourglass-split'
    },
    'APPROVED': {
        text: 'Onaylandı',
        class: 'bg-success-subtle text-success',
        icon: 'check-circle'
    },
    'REJECTED': {
        text: 'Reddedildi',
        class: 'bg-danger-subtle text-danger',
        icon: 'x-circle'
    }
};

const Leave = {
    async get(params) {
        let endpoint = 'leaves/'
        if (params) {
            if (typeof params === 'object') {
                const queryString = Object.keys(params)
                    .map(key => key + '=' + params[key])
                    .join('&')
                return await API.get(`${endpoint}?${queryString}`)
            }
        }
        return await API.get(endpoint)
    },

    formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('tr-TR');
    },

    calculateDuration(startDate, endDate) {
        const start = new Date(startDate);
        const end = new Date(endDate);
        const diffTime = Math.abs(end - start);
        return Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1;
    },

    renderEmptyState(container) {
        container.innerHTML = `
            <div class="text-center py-5">
                <i class="bi bi-inbox text-muted" style="font-size: 3rem;"></i>
                <p class="text-muted">Her yere baktım. Üzgünüm bir sonuç yok.</p>
            </div>
        `;
    },

    renderComponents(data, containerId) {
        const container = document.getElementById(containerId);

        container.innerHTML = `
                <div class="col-md-4 mb-3">
                    <div class="card welcome-card">
                        <div class="card-body">
                            <h6 class="card-subtitle mb-2 text-muted">Kalan İzin Günü</h6>
                            <h3 class="card-title text-primary">${data['left_annual_leave_days']} gün</h3>
                        </div>
                    </div>
                </div>
                <div class="col-md-4 mb-3">
                    <div class="card welcome-card">
                        <div class="card-body">
                            <h6 class="card-subtitle mb-2 text-muted">Bekleyen İzin Talebi</h6>
                            <h3 class="card-title text-warning">${data['pending_leave_request']} talep</h3>
                        </div>
                    </div>
                </div>
                <div class="col-md-4 mb-3">
                    <div class="card welcome-card">
                        <div class="card-body">
                            <h6 class="card-subtitle mb-2 text-muted">Kullanılan İzin</h6>
                            <h3 class="card-title text-success">${data['approved_leave_request']} gün</h3>
                        </div>
                    </div>
                </div>
        `;
    },

    renderTable(data, containerId) {
        const container = document.getElementById(containerId);

        if (!data.results.length) {
            this.renderEmptyState(container);
            return;
        }

        container.innerHTML = `
            <table class="table table-hover border-bottom align-middle">
                <thead class="bg-light">
                    <tr>
                        <th scope="col" class="fw-semibold">İzin Türü</th>
                        <th scope="col" class="fw-semibold">Başlangıç</th>
                        <th scope="col" class="fw-semibold">Bitiş</th>
                        <th scope="col" class="fw-semibold">Süre</th>
                        <th scope="col" class="fw-semibold text-end">Durum</th>
                    </tr>
                </thead>
                <tbody>
                    ${data.results.map(leave => this.renderTableRow(leave)).join('')}
                </tbody>
            </table>
        `;
    },

    renderTableRow(leave) {
        return `
            <tr>
                <td>
                    <div class="d-flex align-items-center">
                        ${reasonMap[leave.reason] || leave.reason}
                    </div>
                </td>
                <td>${this.formatDate(leave.start_date)}</td>
                <td>${this.formatDate(leave.end_date)}</td>
                <td>${this.calculateDuration(leave.start_date, leave.end_date)} gün</td>
                <td class="text-end">
                    <span class="badge ${statusMap[leave.status].class} px-3 py-2">
                        <i class="bi bi-${statusMap[leave.status].icon} me-1"></i>
                        ${statusMap[leave.status].text}
                    </span>
                </td>
            </tr>
        `;
    },

    // Initialize
    init(containerId, containerId2) {
        document.addEventListener('DOMContentLoaded', () => {
            this.fetchAndRender(containerId);
            this.fetchAndComponentRender(containerId2);
            this.setupEventListeners(containerId);
        });
    },

    async fetchAndRender(containerId, filters = {}) {
        try {
            const response = await this.get(filters);
            this.renderTable(response, containerId);
        } catch (error) {
            console.error('Error fetching leave data:', error);
        }
    },

    async fetchAndComponentRender(containerId) {
        try {

            const response = {
                'left_annual_leave_days': 0,
                'pending_leave_request': 0,
                'approved_leave_request': 0,
            }

            const statusPendingResponse = await this.get({"status": "PENDING"})
            const statusApprovedResponse = await this.get({"status": "APPROVED"})

            response['pending_leave_request'] = statusPendingResponse.count
            response['approved_leave_request'] = statusApprovedResponse.count

            this.renderComponents(response, containerId);
        } catch (error) {
            console.error('Error fetching leave data:', error);
        }
    },

    setupEventListeners(containerId) {
        document.getElementById('filterButton')?.addEventListener('click', () => {
            const reason = document.getElementById('reasonFilter')?.value;
            const status = document.getElementById('statusFilter')?.value;

            const filters = {};
            if (reason) filters.reason = reason;
            if (status) filters.status = status;

            this.fetchAndRender(containerId, filters);
        });
    }
};

export default Leave;