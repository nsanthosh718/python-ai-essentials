/**
 * AI Report Generator Node for n8n
 * Generates professional reports with charts and insights
 */

const { IExecuteFunctions, INodeExecutionData, INodeType, INodeTypeDescription } = require('n8n-workflow');
const axios = require('axios');

class AIReportGenerator implements INodeType {
    description: INodeTypeDescription = {
        displayName: 'AI Report Generator',
        name: 'aiReportGenerator',
        icon: 'fa:chart-line',
        group: ['output'],
        version: 1,
        subtitle: '={{$parameter["reportType"]}}',
        description: 'Generate professional AI-powered reports with insights and visualizations',
        defaults: {
            name: 'AI Report Generator',
        },
        inputs: ['main'],
        outputs: ['main'],
        properties: [
            {
                displayName: 'Report Type',
                name: 'reportType',
                type: 'options',
                noDataExpression: true,
                options: [
                    {
                        name: 'Sentiment Analysis Report',
                        value: 'sentiment',
                        description: 'Comprehensive sentiment analysis report',
                    },
                    {
                        name: 'Content Performance Report',
                        value: 'performance',
                        description: 'Content engagement and performance metrics',
                    },
                    {
                        name: 'Trend Analysis Report',
                        value: 'trends',
                        description: 'Market trends and pattern analysis',
                    },
                    {
                        name: 'Competitive Analysis Report',
                        value: 'competitive',
                        description: 'Competitor content and sentiment analysis',
                    },
                    {
                        name: 'Custom Report',
                        value: 'custom',
                        description: 'Custom report with specified parameters',
                    },
                ],
                default: 'sentiment',
            },
            {
                displayName: 'Report Title',
                name: 'reportTitle',
                type: 'string',
                default: 'AI Analysis Report',
                description: 'Title for the generated report',
            },
            {
                displayName: 'Include Charts',
                name: 'includeCharts',
                type: 'boolean',
                default: true,
                description: 'Include data visualizations in the report',
            },
            {
                displayName: 'Chart Types',
                name: 'chartTypes',
                type: 'multiOptions',
                options: [
                    {
                        name: 'Sentiment Pie Chart',
                        value: 'sentiment_pie',
                    },
                    {
                        name: 'Trend Line Chart',
                        value: 'trend_line',
                    },
                    {
                        name: 'Confidence Histogram',
                        value: 'confidence_hist',
                    },
                    {
                        name: 'Source Breakdown',
                        value: 'source_breakdown',
                    },
                    {
                        name: 'Time Series',
                        value: 'time_series',
                    },
                ],
                default: ['sentiment_pie', 'trend_line'],
                displayOptions: {
                    show: {
                        includeCharts: [true],
                    },
                },
            },
            {
                displayName: 'Output Format',
                name: 'outputFormat',
                type: 'options',
                options: [
                    {
                        name: 'JSON',
                        value: 'json',
                        description: 'Structured JSON report',
                    },
                    {
                        name: 'HTML',
                        value: 'html',
                        description: 'HTML report with embedded charts',
                    },
                    {
                        name: 'PDF',
                        value: 'pdf',
                        description: 'Professional PDF report',
                    },
                    {
                        name: 'Markdown',
                        value: 'markdown',
                        description: 'Markdown formatted report',
                    },
                ],
                default: 'json',
            },
            {
                displayName: 'Include Recommendations',
                name: 'includeRecommendations',
                type: 'boolean',
                default: true,
                description: 'Include AI-generated recommendations',
            },
            {
                displayName: 'Executive Summary',
                name: 'executiveSummary',
                type: 'boolean',
                default: true,
                description: 'Include executive summary section',
            },
            {
                displayName: 'Brand Name',
                name: 'brandName',
                type: 'string',
                default: '',
                placeholder: 'Your Company',
                description: 'Brand name to include in the report',
            },
            {
                displayName: 'Custom Sections',
                name: 'customSections',
                type: 'fixedCollection',
                placeholder: 'Add Section',
                typeOptions: {
                    multipleValues: true,
                },
                default: {},
                options: [
                    {
                        name: 'sections',
                        displayName: 'Section',
                        values: [
                            {
                                displayName: 'Section Title',
                                name: 'title',
                                type: 'string',
                                default: '',
                            },
                            {
                                displayName: 'Section Content',
                                name: 'content',
                                type: 'string',
                                typeOptions: {
                                    rows: 3,
                                },
                                default: '',
                            },
                        ],
                    },
                ],
                displayOptions: {
                    show: {
                        reportType: ['custom'],
                    },
                },
            },
        ],
    };

    async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
        const items = this.getInputData();
        const returnData: INodeExecutionData[] = [];

        const reportType = this.getNodeParameter('reportType', 0) as string;
        const reportTitle = this.getNodeParameter('reportTitle', 0) as string;
        const includeCharts = this.getNodeParameter('includeCharts', 0) as boolean;
        const chartTypes = this.getNodeParameter('chartTypes', 0) as string[];
        const outputFormat = this.getNodeParameter('outputFormat', 0) as string;
        const includeRecommendations = this.getNodeParameter('includeRecommendations', 0) as boolean;
        const executiveSummary = this.getNodeParameter('executiveSummary', 0) as boolean;
        const brandName = this.getNodeParameter('brandName', 0) as string;

        try {
            // Aggregate all input data
            const aggregatedData = items.map(item => item.json);

            const report = await this.generateReport({
                data: aggregatedData,
                reportType,
                reportTitle,
                includeCharts,
                chartTypes,
                outputFormat,
                includeRecommendations,
                executiveSummary,
                brandName,
            });

            returnData.push({
                json: {
                    report: report,
                    reportType: reportType,
                    generatedAt: new Date().toISOString(),
                    itemsAnalyzed: items.length,
                },
            });

        } catch (error) {
            if (this.continueOnFail()) {
                returnData.push({
                    json: {
                        error: error.message,
                        reportType: reportType,
                    },
                });
            } else {
                throw error;
            }
        }

        return [returnData];
    }

    private async generateReport(params: any): Promise<any> {
        const apiEndpoint = 'http://localhost:8082/api';
        
        const response = await axios.post(`${apiEndpoint}/generate_report`, {
            ...params,
        });

        return response.data;
    }
}

module.exports = { nodeClass: AIReportGenerator };