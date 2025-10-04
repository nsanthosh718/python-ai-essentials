/**
 * AI Content Analyzer Node for n8n
 * Commercial-grade node for sentiment analysis and content insights
 */

const { IExecuteFunctions, INodeExecutionData, INodeType, INodeTypeDescription } = require('n8n-workflow');
const axios = require('axios');

class AIContentAnalyzer implements INodeType {
    description: INodeTypeDescription = {
        displayName: 'AI Content Analyzer',
        name: 'aiContentAnalyzer',
        icon: 'fa:brain',
        group: ['transform'],
        version: 1,
        subtitle: '={{$parameter["operation"]}}',
        description: 'Analyze content sentiment, extract insights, and generate reports using AI',
        defaults: {
            name: 'AI Content Analyzer',
        },
        inputs: ['main'],
        outputs: ['main'],
        credentials: [
            {
                name: 'aiContentAnalyzerApi',
                required: false,
            },
        ],
        properties: [
            {
                displayName: 'Operation',
                name: 'operation',
                type: 'options',
                noDataExpression: true,
                options: [
                    {
                        name: 'Analyze Sentiment',
                        value: 'analyzeSentiment',
                        description: 'Analyze sentiment of text content',
                        action: 'Analyze sentiment of text content',
                    },
                    {
                        name: 'Extract Insights',
                        value: 'extractInsights',
                        description: 'Extract key insights and trends',
                        action: 'Extract insights from content',
                    },
                    {
                        name: 'Generate Report',
                        value: 'generateReport',
                        description: 'Generate comprehensive analysis report',
                        action: 'Generate analysis report',
                    },
                    {
                        name: 'Batch Analysis',
                        value: 'batchAnalysis',
                        description: 'Analyze multiple content items',
                        action: 'Perform batch content analysis',
                    },
                ],
                default: 'analyzeSentiment',
            },
            {
                displayName: 'Content Field',
                name: 'contentField',
                type: 'string',
                default: 'content',
                placeholder: 'content',
                description: 'Field containing the text content to analyze',
                displayOptions: {
                    show: {
                        operation: ['analyzeSentiment', 'extractInsights', 'batchAnalysis'],
                    },
                },
            },
            {
                displayName: 'Analysis Type',
                name: 'analysisType',
                type: 'options',
                options: [
                    {
                        name: 'Basic Sentiment',
                        value: 'basic',
                        description: 'Fast rule-based sentiment analysis',
                    },
                    {
                        name: 'ML Enhanced',
                        value: 'ml',
                        description: 'Machine learning powered analysis',
                    },
                    {
                        name: 'Deep Analysis',
                        value: 'deep',
                        description: 'Comprehensive analysis with insights',
                    },
                ],
                default: 'ml',
                displayOptions: {
                    show: {
                        operation: ['analyzeSentiment', 'batchAnalysis'],
                    },
                },
            },
            {
                displayName: 'Include Confidence Score',
                name: 'includeConfidence',
                type: 'boolean',
                default: true,
                description: 'Whether to include confidence scores in results',
            },
            {
                displayName: 'API Endpoint',
                name: 'apiEndpoint',
                type: 'string',
                default: 'http://localhost:8082/api',
                description: 'AI Content Analyzer API endpoint',
            },
        ],
    };

    async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
        const items = this.getInputData();
        const returnData: INodeExecutionData[] = [];
        
        const operation = this.getNodeParameter('operation', 0) as string;
        const contentField = this.getNodeParameter('contentField', 0) as string;
        const analysisType = this.getNodeParameter('analysisType', 0) as string;
        const includeConfidence = this.getNodeParameter('includeConfidence', 0) as boolean;
        const apiEndpoint = this.getNodeParameter('apiEndpoint', 0) as string;

        for (let i = 0; i < items.length; i++) {
            try {
                const item = items[i];
                let result: any = {};

                switch (operation) {
                    case 'analyzeSentiment':
                        result = await this.analyzeSentiment(
                            item.json[contentField] as string,
                            analysisType,
                            includeConfidence,
                            apiEndpoint
                        );
                        break;

                    case 'extractInsights':
                        result = await this.extractInsights(
                            item.json[contentField] as string,
                            apiEndpoint
                        );
                        break;

                    case 'generateReport':
                        result = await this.generateReport(item.json, apiEndpoint);
                        break;

                    case 'batchAnalysis':
                        result = await this.batchAnalysis(
                            items.map(item => item.json[contentField] as string),
                            analysisType,
                            apiEndpoint
                        );
                        break;
                }

                returnData.push({
                    json: {
                        ...item.json,
                        aiAnalysis: result,
                        processedAt: new Date().toISOString(),
                    },
                });

            } catch (error) {
                if (this.continueOnFail()) {
                    returnData.push({
                        json: {
                            ...items[i].json,
                            error: error.message,
                        },
                    });
                    continue;
                }
                throw error;
            }
        }

        return [returnData];
    }

    private async analyzeSentiment(
        content: string,
        analysisType: string,
        includeConfidence: boolean,
        apiEndpoint: string
    ): Promise<any> {
        const response = await axios.post(`${apiEndpoint}/analyze_text`, {
            text: content,
            analysis_type: analysisType,
            include_confidence: includeConfidence,
        });

        return {
            sentiment: response.data.sentiment,
            confidence: response.data.confidence,
            analysis_type: analysisType,
            processed_at: new Date().toISOString(),
        };
    }

    private async extractInsights(content: string, apiEndpoint: string): Promise<any> {
        const response = await axios.post(`${apiEndpoint}/extract_insights`, {
            text: content,
        });

        return {
            insights: response.data.insights || [],
            keywords: response.data.keywords || [],
            entities: response.data.entities || [],
            summary: response.data.summary || '',
        };
    }

    private async generateReport(data: any, apiEndpoint: string): Promise<any> {
        const response = await axios.post(`${apiEndpoint}/generate_report`, {
            data: data,
        });

        return {
            report_id: response.data.report_id,
            summary: response.data.summary,
            recommendations: response.data.recommendations || [],
            charts: response.data.charts || {},
        };
    }

    private async batchAnalysis(
        contents: string[],
        analysisType: string,
        apiEndpoint: string
    ): Promise<any> {
        const response = await axios.post(`${apiEndpoint}/batch_analyze`, {
            texts: contents,
            analysis_type: analysisType,
        });

        return {
            total_analyzed: response.data.total_analyzed,
            overall_sentiment: response.data.overall_sentiment,
            sentiment_breakdown: response.data.sentiment_breakdown,
            batch_insights: response.data.insights || [],
        };
    }
}

module.exports = { nodeClass: AIContentAnalyzer };